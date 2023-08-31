from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from werkzeug import Response

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ek8xWAoO3BuHJmEtjGILcLi23COMQ9teaDmF84luxy7z04P6VHCV7iZrnt6mqSRJf44V55i9lrfhxLmrvNfG0i9q'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:nopass@localhost:3306/python_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


@app.errorhandler(Exception)
def handle_exception(e):
    response = Response()
    if hasattr(e, 'code'):
        code = e.code
    else:
        code = 500

    if hasattr(e, 'message'):
        message = e.message
    else:
        message = str(e)

    response.data = json.dumps({
        "data": {},
        "code": code,
        "message": message,
    })
    response.content_type = "application/json"
    return response
