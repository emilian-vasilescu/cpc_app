# decorator for verifying the JWT
from functools import wraps

import jwt
from flask import request, jsonify

from Models.User import User
from app import app


def check_jwt_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return {'error': 'Token is missing !!'}, 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(jwt=token, key=app.config['SECRET_KEY'], algorithms="HS256")
            current_user = User.query \
                .filter_by(public_id=data['public_id']) \
                .first()
        except Exception as e:
            return {'error': str(e)}, 401
        # returns the current logged in users context to the routes
        return f(*args, current_user, **kwargs)

    return decorated
