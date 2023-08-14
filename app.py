# creates Flask object
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = 'ek8xWAoO3BuHJmEtjGILcLi23COMQ9teaDmF84luxy7z04P6VHCV7iZrnt6mqSRJf44V55i9lrfhxLmrvNfG0i9q'
# database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:nopass@localhost:3306/python_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object
db = SQLAlchemy(app)
