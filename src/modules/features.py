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
from .models import db, WishlistItem, Wishlist, User, SearchEntry
import requests
from .scraper import driver, filter

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
    """Return a list of wishlist names for the user."""
    user = User.query.filter_by(username=username).first()
    if user:
        return [wishlist.name for wishlist in user.wishlists]
    return []

def create_wishlist(username, wishlist_name):
    """Create a new wishlist for the user."""
    user = User.query.filter_by(username=username).first()
    if user:
        new_wishlist = Wishlist(name=wishlist_name, user_id=user.id)
        db.session.add(new_wishlist)
        db.session.commit()
        return True
    return False

def remove_wishlist_item(username, wishlist_name, item_id):
    """Remove an item from a wishlist."""
    item = WishlistItem.query.get(item_id)
    if item and item.wishlist.user.username == username:  
        db.session.delete(item)
        db.session.commit()
        return True
    return False


def wishlist_add_item(username, wishlist_name, item_data):
    user = User.query.filter_by(username=username).first()
    wishlist = Wishlist.query.filter_by(user_id=user.id, name=wishlist_name).first()
    if not wishlist:
        return False  

    price = item_data.get('price')
    if isinstance(price, str) and (price.upper() == 'N/A' or price == ''):
        item_data['price'] = None
    elif price is not None:
        try:
            item_data['price'] = float(price)
        except ValueError:
            item_data['price'] = None  

    new_item = WishlistItem(
        wishlist_id=wishlist.id,
        title=item_data['title'],
        price=item_data['price'],
        link=item_data.get('link'),
        website=item_data.get('website'),
        rating=item_data.get('rating')
    )
    db.session.add(new_item)
    db.session.commit()
    return True


def read_wishlist(username, wishlist_name):
    """Read all items from a specific wishlist."""
    user = User.query.filter_by(username=username).first()
    wishlist = Wishlist.query.filter_by(user_id=user.id, name=wishlist_name).first()
    if wishlist:
        return [{'title': item.title, 'price': item.price, 'link': item.link, 'website': item.website, 'rating': item.rating} for item in wishlist.items]
    return []

def share_wishlist(username, wishlist_name, email_receiver):
    """Share wishlist via email."""
    items = read_wishlist(username, wishlist_name)
    if items:
        try:
            email_sender = current_app.config['MAIL_USERNAME']
            email_password = current_app.config['MAIL_PASSWORD']
            subject = f"{username}'s Wishlist"
            body = "\n".join([f"{i+1}. {item['title']} - {item['link']}" for i, item in enumerate(items)])

            message = EmailMessage()
            message.set_content(body)
            message['Subject'] = subject
            message['From'] = email_sender
            message['To'] = email_receiver

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(email_sender, email_password)
            server.send_message(message)
            server.quit()
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    return False

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

def create_search_entry(username, search_term):
    user = User.query.filter_by(username=username).first()
    if user:
        new_search_entry = SearchEntry(user_id=user.id, search_term=search_term)
        db.session.add(new_search_entry)
        db.session.commit()



def get_user_searches_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.searches
    return []

def get_related_products_from_chatgpt(search_term):
    openai_api_key = os.getenv('OPENAI_API_KEY') 
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    prompt = f"List three related product titles for the search term '{search_term}', each on a new line. Limit the product titles to three-four words."
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": prompt}]
    }

    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        suggestions = response_data['choices'][0]['message']['content'].strip().split('\n')
        clean_suggestions = [s.strip().split('. ')[-1] for s in suggestions if s.strip()]
        return clean_suggestions
    else:
        print("Failed to get suggestions:", response.text)
        return []

def generate_product_recommendations(username):
    user = User.query.filter_by(username=username).first()
    if not user or not user.searches:
        return []

    last_search = user.searches[-1].search_term

    related_products = get_related_products_from_chatgpt(last_search)
    return related_products[:3]  


def search_products(query):
    currency = 'USD'  
    num = 3  
    return driver(query, currency, num, df_flag=0, ui=True)
