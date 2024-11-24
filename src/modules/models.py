from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    wishlists = db.relationship('Wishlist', backref='user', lazy=True)
    searches = db.relationship('SearchEntry', backref='user', lazy=True)
    __tablename__ = 'users'

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items = db.relationship('WishlistItem', backref='wishlist', lazy=True)
    __tablename__ = 'wishlist'

class WishlistItem(db.Model):
    __tablename__ = 'wishlist_item'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=True)
    link = db.Column(db.String(300))
    website = db.Column(db.String(100))
    rating = db.Column(db.String(10))
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlist.id'), nullable=False)
    
    __table_args__ = {'extend_existing': True}

class SearchEntry(db.Model):
    __tablename__ = 'search_entries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    search_term = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

