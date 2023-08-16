# creates Flask object
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ek8xWAoO3BuHJmEtjGILcLi23COMQ9teaDmF84luxy7z04P6VHCV7iZrnt6mqSRJf44V55i9lrfhxLmrvNfG0i9q'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:nopass@localhost:3306/python_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "message": e.description,
    })
    response.content_type = "application/json"
    return response
