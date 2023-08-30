# decorator for verifying the JWT
from functools import wraps

import jwt
from flask import request

from Exceptions.exceptions import AuthenticationException
from Models.user import User
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
            raise AuthenticationException('Token is missing !!')

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(jwt=token, key=app.config['SECRET_KEY'], algorithms="HS256")
            current_user = User.query \
                .filter_by(public_id=data['public_id']) \
                .first()

            if current_user is None:
                raise AuthenticationException('Token is ok but, user doesn\'t exist')

        except Exception as e:
            return AuthenticationException(str(e))
        # returns the current logged in users context to the routes
        return f(*args, current_user, **kwargs)

    return decorated
