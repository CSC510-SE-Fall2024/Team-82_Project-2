"""
Copyright (C) Team-82_Project-2
 
Licensed under the MIT License.
See the LICENSE file in the project root for the full license information.
"""

import os
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

from flask import Flask, session, render_template, request, redirect, url_for, make_response, jsonify
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

from .scraper import driver, filter, get_currency_rate, convert_currency
from .features import create_user, check_user, db_check_user, db_create_user, wishlist_add_item, read_wishlist, remove_wishlist_item, share_wishlist
from .config import Config
from .models import db
import secrets
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import StringIO
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

# Load environment variables from .env file
load_dotenv() 

app = Flask(__name__, template_folder=".")

app.secret_key = Config.SECRET_KEY

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    try:
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        receiver_email = email

        # Ensure credentials are available
        if not sender_email or not sender_password:
            raise EnvironmentError("SENDER_EMAIL and SENDER_PASSWORD must be set in the environment.")

        subject = 'Secure Login to Slash - Your OTP Code'
        body = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background: #ffffff;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background-color: #4CAF50;
                    padding: 20px;
                    text-align: center;
                    color: white;
                }}
                .header img {{
                    max-width: 100px;
                }}
                .content {{
                    padding: 20px;
                }}
                .otp {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #4CAF50;
                    text-align: center;
                }}
                .footer {{
                    background-color: #f1f1f1;
                    text-align: center;
                    padding: 10px;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Slash</h1>
                </div>
                <div class="content">
                    <p>Dear User,</p>
                    <p>Your One-Time Password (OTP) for secure login to Slash is:</p>
                    <div class="otp">{otp}</div>
                    <p>This OTP is valid for the next 5 minutes. If you did not request this code, please disregard this message.</p>
                    <p>Thank you for choosing Slash for your smart shopping experience.</p>
                </div>
                <div class="footer">
                    &copy; {2024} Slash. All rights reserved.<br>
                    <a href="http://localhost:5000" style="color: #4CAF50;">Visit Slash</a>
                </div>
            </div>
        </body>
        </html>
        '''

        # Create the email
        message = MIMEMultipart("alternative")
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Attach the HTML email body
        message.attach(MIMEText(body, "html"))

        # Send the email using a secure SSL context
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("Email sent successfully.")
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False







# OAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'), # Fetch client_id from .env
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),  # Fetch client_secret from .env
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    redirect_uri='http://localhost:5000/google/callback',
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    client_kwargs={'scope': 'openid profile email'}
)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# Create the tables
with app.app_context():
    db.create_all()

@app.route('/')
def landingpage():
    login = False
    if 'username' in session:
        login = True
    return render_template("./static/landing.html", login=login)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            return 'Username and Password are required', 400

        if db_check_user(username, password):

            # Generate and send OTP
            otp = generate_otp()
            session['login_otp'] = otp
            session['login_otp_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            session['pending_username'] = username
            
            if send_otp_email(username, otp):
                return render_template("./static/landing.html", show_otp=True)
            else:
                return 'Error sending OTP email', 500
        else:
            return render_template("./static/landing.html", login=False, invalid=True), 401
    
    elif session.get('oauth'):
        return redirect(url_for('login'))
    return render_template('./static/login.html')
    


@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    entered_otp = request.form['otp']
    stored_otp = session.get('login_otp')
    otp_time = datetime.strptime(session.get('login_otp_time'), '%Y-%m-%d %H:%M:%S')
    
    # Check if OTP is expired (5 minutes validity)
    if datetime.now() - otp_time > timedelta(minutes=5):
        return render_template("./static/landing.html", otp_error="OTP expired")
    
    if entered_otp == stored_otp:
        # Clear OTP session data
        session.pop('login_otp', None)
        session.pop('login_otp_time', None)
        
        # Set the actual username in session
        session['username'] = session.pop('pending_username', None)
        return redirect(url_for('login'))
    else:
        return render_template("./static/landing.html", show_otp=True, otp_error="Invalid OTP")

@app.route('/resend-otp', methods=['POST'])
def resend_otp():
    username = session.get('pending_username')
    if username:
        otp = generate_otp()
        session['login_otp'] = otp
        session['login_otp_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if send_otp_email(username, otp):
            return render_template("./static/landing.html", show_otp=True, otp_message="New OTP sent")
        else:
            return 'Error sending OTP email', 500
    return 'No pending login', 400


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if db_create_user(username, password):
            session['username'] = username
            return redirect(url_for('login'))
        else:
            return render_template("./static/landing.html", login=False, invalid=True)
            
    return render_template('./static/login.html')

@app.route('/login/google')
def google_login():
    # Redirect the user to Google's OAuth page
    redirect_uri = 'http://localhost:5000/google/callback'
    nonce = secrets.token_urlsafe(16)
    session['nonce'] = nonce
    return google.authorize_redirect(redirect_uri,  nonce=nonce)


@app.route('/google/callback')
def google_callback():
    try:
        token = google.authorize_access_token()
        # Get the nonce from the session
        nonce = session.pop('nonce', None)  # Remove the nonce from the session
        user_info = google.parse_id_token(token, nonce=nonce)  # Pass the nonce here
        session['username'] = user_info['email']
        db_create_user(session["username"], "")
        return redirect(url_for('login'))
    except Exception as e:
        return f"Error: {e}"


@app.route('/wishlist')
def wishlist():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    wishlist_items = read_wishlist(username, "default")  # Assume default wishlist for simplicity
    return render_template('./static/wishlist.html', data=wishlist_items)

@app.route('/share', methods=['POST'])
def share():
    username = session['username']
    wishlist_name = "default"
    email_receiver = request.form['email']
    share_wishlist(username, wishlist_name, email_receiver)
    return redirect(url_for('wishlist'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('./static/landing.html')

@app.route("/search", methods=["POST", "GET"])
def product_search(new_product="", sort=None, currency=None, num=None, min_price=None, max_price=None, min_rating=None, website=None):
    try:
        product = request.args.get("product_name")
        if product is None:
            product = new_product

        data = driver(product, currency, num, 0, False, None, True, sort, website)

        if min_price is not None or max_price is not None or min_rating is not None:
            data = filter(data, min_price, max_price, min_rating)
        return render_template("./static/result.html", data=data, prod=product, total_pages=len(data)//20)
    except Exception as e:
        app.logger.error(f"Error during product search: {e}")
        return render_template("error.html", error=str(e)), 500


@app.route("/filter", methods=["POST", "GET"])
def product_search_filtered():
    try:
        product = request.args.get("product_name")
        sort = request.form["sort"]
        currency = request.form["currency"]
        website = request.form.get("website", "all")

        min_price = request.form["min_price"]
        max_price = request.form["max_price"]
        min_rating = request.form["min_rating"]

        try:
            min_price = float(min_price)
        except:
            min_price = None

        try:
            max_price = float(max_price)
        except:
            max_price = None

        try:
            min_rating = float(min_rating)
        except:
            min_rating = None

        if sort == "default":
            sort = None
        if currency == "usd":
            currency = None

        return product_search(product, sort, currency, None, min_price, max_price, min_rating, website)
    except Exception as e:
        app.logger.error(f"Error during filtered product search: {e}")
        return render_template("./templates/error.html", error=str(e)), 500

@app.route("/add-wishlist-item", methods=["POST"])
def add_wishlist_item():
    try:
        username = session['username']
        item_data = request.form.to_dict()
        wishlist_name = 'default'

        if 'price' in item_data:
            price = item_data['price'].replace('$', '').strip()
            if price == '' or price == 'N/A' or price is None:
                item_data['price'] = None  
            else:
                try:
                    item_data['price'] = float(price)  
                except ValueError:
                    return jsonify(error="Invalid price format"), 400  

        if wishlist_add_item(username, wishlist_name, item_data):
            return redirect(url_for('wishlist'))
        else:
            return "Error adding item", 400
    except Exception as e:
        app.logger.error(f"Error adding item: {e}")
        return jsonify(error=str(e)), 500


@app.route("/delete-wishlist-item", methods=["POST"])
def delete_wishlist_item():  
    try:
        username = session['username']
        item_id = int(request.form["index"])  
        wishlist_name = 'default'
        if remove_wishlist_item(username, wishlist_name, item_id): 
            return redirect(url_for('wishlist'))
        else:
            return "Error removing item", 400
    except Exception as e:
        app.logger.error(f"Error removing item: {e}")
        return jsonify(error=str(e)), 500
    
@app.cli.command("init-db")
def init_db():
    """Clear existing data and create new tables."""
    db.drop_all()
    db.create_all()
    print("Initialized the database.")

@app.route('/export_csv')
def export_csv():
    product_name = request.args.get('product_name')
    sort = request.args.get('sort')
    currency = request.args.get('currency')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    min_rating = request.args.get('min_rating')

    # Call the driver function to get the data
    results = driver(product_name, 'USD', None, 0, False, None, True, sort)
    results = filter(results, 0, 100000, 0)
    
    product_df = pd.DataFrame(columns=['Sr No.', 'Title', 'Link', 'Rating', 'Price'])

    # Write the data
    rate = None
    if currency:
        rate = get_currency_rate('USD', currency)
    for index, product in enumerate(results, start=1):
        price = product.get('price', '')
        if rate and price != '':
            price = convert_currency(price, currency, rate)
        row = [
            index,
            product.get('title', ''),
            product.get('link', ''),
            product.get('rating', 'N/A'),
            price
        ]
        product_df.loc[len(product_df)] = row
    
    # Create a string buffer
    buffer = StringIO()
    
    # Write the DataFrame to the buffer
    product_df.to_csv(buffer, index=False)
    # Create the HTTP response with CSV data
    output = make_response(buffer.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename={product_name}.csv"
    output.headers["Content-type"] = "text/csv"
    
    return output

@app.route('/product_comparison')
def product_comparison():
    return render_template('./static/product_comparison.html')
    
    

if __name__ == '__main__':
    app.run(debug=True)
