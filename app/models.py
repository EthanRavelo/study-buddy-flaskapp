from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coins = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Item(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(10000))
    url = db.Column(db.String(10000))
    category = db.Column(db.String(1000))
    active = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class All_Items(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(10000))
    url = db.Column(db.String(10000))
    category = db.Column(db.String(1000))
    price = db.Column(db.Integer)


class currentData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    subject = db.Column(db.String(150))
    messaging = db.Column(db.Boolean)
    username = db.Column(db.String(1000))
    time = db.Column(db.Integer)
    avatar = db.Column(db.String(10000))
    spot1 = db.Column(db.String(10000))
    spot2 = db.Column(db.String(10000))
    spot3 = db.Column(db.String(10000))
    spot4 = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    message = db.Column(db.String(500))
    sender_id = db.Column(db.String(50))
    receiver_id = db.Column(db.String(50))


class Chat_Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    user_id = db.Column(db.String(50))


class New_Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.String(50))
    target_id = db.Column(db.String(50))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    student_id = db.Column(db.Integer)
    school = db.Column(db.String(150))
    logged_in = db.Column(db.String(10))
    coins = db.relationship('Coin')
    items = db.relationship('Item')
    currentData = db.relationship('currentData')
    logged_in = db.Column(db.String(10))

