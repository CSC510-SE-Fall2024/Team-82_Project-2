"""
Copyright (C) Team-82_Project-2
 
Licensed under the MIT License.
See the LICENSE file in the project root for the full license information.
"""

import json
import os
import pandas as pd
import numpy as np
import re
import ssl
import smtplib
from pathlib import Path
from .config import Config
import bcrypt

from . import scraper
from email.message import EmailMessage
from .models import db, User

#All db_* prefix functions use sqlite db instead of existing file approach

# path for user profiles and their wish lists
users_main_dir = Path(__file__).parent.parent / "users"
users_main_dir.mkdir(parents=True, exist_ok=True)

def usr_dir(username):
    return users_main_dir / username

def create_user(username, password):
    user_dir = usr_dir(username)
    if os.path.exists(user_dir): # user already exist
        stored_password = get_credentials(username)
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return True
        #if password == get_credentials(username):
            #return True
        else:
            return False
    else: # create new user
        user_dir.mkdir(parents=True, exist_ok=True)
        create_credentials(username, password)
        create_wishlist(username, 'default')
        return True
    
def db_create_user(username, password):
    user_dir = usr_dir(username)
    """Create a new user or authenticate existing user using database."""
    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    
    if existing_user:
        # If user exists, verify password
        return bcrypt.checkpw(
            password.encode('utf-8'),
            existing_user.password.encode('utf-8')
        )
    
    # Create new user
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    new_user = User(
        username=username,
        password=hashed_password
    )
    
    # Save to database
    db.session.add(new_user)
    db.session.commit()
    
    user_dir.mkdir(parents=True, exist_ok=True)
    # Create default wishlist
    create_wishlist(username, 'default')
    
    return True

def check_user(username, password):
    user_dir = usr_dir(username)
    if os.path.exists(user_dir): # user already exist
        stored_password = get_credentials(username)
        if stored_password:
            return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
    else: 
        return False        
    
def db_check_user(username, password):
    """Check if the user exists and the password is correct."""
    user = User.query.filter_by(username=username).first()
    if user:
        # Compare the hashed password stored in the database with the password provided by the user
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return True
    return False


def list_users():
    ls = os.listdir(users_main_dir)
    list_of_users = list(filter(lambda u: os.path.isdir(os.path.join(users_main_dir, u)), ls))
    return list_of_users

def create_wishlist(username, wishlist_name):
    wishlist_path = usr_dir(username) / (wishlist_name + ".csv")
    open(wishlist_path, "a").close()

def create_credentials(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cred_path = usr_dir(username) / ("cred.csv")
    open(cred_path, "a").close()
    item_data = {
        "username": username,
        "password": hashed_password.decode('utf-8'),
    }
    item_data = pd.DataFrame([item_data])
    item_data.to_csv(cred_path, index=False, header=item_data.columns)

def get_credentials(username):
    cred_path = usr_dir(username) / ("cred.csv")
    if os.path.exists(cred_path):
        try:
            csv = pd.read_csv(cred_path)
            row = csv.iloc[0]
            return str(row['password'])
        except Exception as e:
            print(f"Error reading credentials: {e}")
            return ''
    else:
        return '' 

def list_wishlists(username):
    user_dir = usr_dir(username)
    wishlists = list(map(lambda w: w.replace(".csv", ""), os.listdir(user_dir)))
    return wishlists

def delete_wishlist(username, wishlist_name):
    wishlist_path = usr_dir(username) / (wishlist_name + ".csv")
    wishlist_path.unlink(missing_ok=True)

def wishlist_add_item(username, wishlist_name, item_data):
    if isinstance(item_data, dict):
        item_data = pd.DataFrame([item_data])
    wishlist_path = usr_dir(username) / (wishlist_name + ".csv")
    if os.path.exists(wishlist_path) and (os.path.getsize(wishlist_path) > 0 ):
        old_data = pd.read_csv(wishlist_path)
    else:
        old_data = pd.DataFrame()
    #if self.df.title[indx] not in old_data:
    final_data = pd.concat([old_data, item_data])
    final_data.to_csv(wishlist_path, index=False, header=item_data.columns)

def read_wishlist(username, wishlist_name):
    wishlist_path = usr_dir(username) / (wishlist_name + ".csv")
    if os.path.exists(wishlist_path):
        try:
            csv = pd.read_csv(wishlist_path)
            for index,obj in csv.iterrows():
                new_price = update_price(obj['link'],obj['website'],obj['price'])
                csv.at[index, 'price'] = new_price
            return csv
        except Exception:
            return pd.DataFrame()
    else:
        return None # wishlist not found

def share_wishlist(username, wishlist_name, email_receiver):
    wishlist_path = usr_dir(username) / (wishlist_name + ".csv")
    if os.path.exists(wishlist_path):
        try:
            email_sender = 'slash.se23@gmail.com'
            email_password = Config.EMAIL_PASS

            subject = ' slash wishlist of ' + username

            df = pd.read_csv(wishlist_path)
            links_list = df['link'].astype(str).str.cat(sep=' ')
            body = "\n".join([f"{i}. {link}" for i, link in enumerate(links_list.split(), start=1)])

            em = EmailMessage()
            em['from'] = email_sender
            em['to'] = email_receiver
            em['subject'] = subject
            em.set_content(body)
            

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

        except Exception:
            return 'failed to send email'
    else:
        return None # wishlist not found

def wishlist_remove_list(username, wishlist_name, indx):
    wishlist_path = usr_dir(username) / (wishlist_name + ".csv")
    old_data = read_wishlist(username, wishlist_name)
    old_data = old_data.drop(index=indx)
    old_data.to_csv(wishlist_path, index=False, header=old_data.columns)

def find_currency(price):
    currency = re.match(r'^[a-zA-Z]{3,5}', price)
    return currency.group() if currency else currency

def update_price(link,website,price):
    currency = find_currency(price)
    updated_price = price
    if website == "amazon":
        scraped_price = scraper.amazon_scraper(link).strip()
        if scraped_price:
            updated_price = scraper.getCurrency(currency,scraped_price) if currency is not None else scraped_price
    if website == "google":
        scraped_price = scraper.google_scraper(link).strip()
        if scraped_price:
            updated_price = scraper.getCurrency(currency,scraped_price) if currency is not None else scraped_price
    if website == "BJS":
        pass
    if website == "Etsy":
        pass
    if website == "walmart":
        scraped_price = scraper.walmart_scraper(link).strip()
        if scraped_price:
            updated_price = scraper.getCurrency(currency,scraped_price) if currency is not None else scraped_price
    if website == "ebay":
        scraped_price = scraper.ebay_scraper(link).strip()
        if scraped_price:
            updated_price = scraper.getCurrency(currency,scraped_price) if currency is not None else scraped_price
    if website == "bestbuy":
        scraped_price = scraper.bestbuy_scraper(link).strip()
        if scraped_price:
            updated_price = scraper.getCurrency(currency,scraped_price) if currency is not None else scraped_price       
    if website == "target":
        scraped_price = scraper.target_scraper(link).strip()
        if scraped_price:
            updated_price = scraper.getCurrency(currency,scraped_price) if currency is not None else scraped_price      
    return updated_price
