from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

# Load configurations from config.py
app.config.from_object('config')

# Initialize MySQL
mysql = MySQL()
mysql.init_app(app)

# Importing routes after the Flask app is initialized
from app import views
