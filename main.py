from website import create_app
from flask import Flask 
from flask_socketio import SocketIO, send

import pusher
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Set the upload folder as the static folder in app directory
    UPLOAD_FOLDER = 'app/static'

app = create_app()


pusher_client = pusher.Pusher(
  app_id='1429475',
  key='2dd35a38909a3742c906',
  secret='31f2abcb2629c011c24d',
  cluster='us2',
  ssl=True
)

if __name__ == '__main__':
    app.run(debug=True) 

    
    