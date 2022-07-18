# Authors: CS For Insight (Summer19 - JG)
from flask_sqlalchemy import SQLAlchemy

try:
    from flask import Flask
except:
    print("could not import Flask from flask")

from config import Config

app = Flask(__name__, static_url_path='')
app.config.from_object(Config)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'

from app import routes