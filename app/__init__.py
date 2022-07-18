# Authors: CS For Insight (Summer19 - JG)
import os
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
try:
    from flask import Flask
except:
    print("could not import Flask from flask")

from config import Config
from flask_socketio import SocketIO, send

app = Flask(__name__, static_url_path='')
app.config.from_object(Config)


db = SQLAlchemy(app)
DB_NAME = "database.db"

app.config['SECRET_KEY'] = 'abcdefghijklmnop'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handle_message(message):
    print("Recieved message: " + message)
    if message != "User connected":
        send(message, broadcast=True)

import pusher
pusher_client = pusher.Pusher(
  app_id='1429475',
  key='2dd35a38909a3742c906',
  secret='31f2abcb2629c011c24d',
  cluster='us2',
  ssl=True
)
pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})

from .models import User
from app import routes


def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

create_database(app)


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))