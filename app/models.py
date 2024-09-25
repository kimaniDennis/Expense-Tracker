from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)



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
