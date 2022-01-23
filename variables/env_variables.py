import os

CLIENT_SECRET = os.environ['CLIENT_SECRET']
DATABASE_URL = os.environ['DATABASE_URL']
BOT_TOKEN = os.environ['BOT_TOKEN']
FERNET_KEY = os.environ['FERNET_KEY']
FLASK_SECRET_KEY = os.environ['FLASK_SECRET_KEY']
PORT = int(os.environ.get('PORT', 5000))
DEBUG_MODE = os.environ.get('DEBUG_MODE', 0)
