from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Float, nullable = False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String)
    type = db.Column(db.String)



class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
