from datetime import datetime, timedelta
import jwt
from flask import request
from werkzeug.security import check_password_hash

from Controllers.base_controller import BaseController
from Exceptions.exceptions import AuthenticationException
from Models.user import User
from app import app


class LoginController(BaseController):
    def post(self):
        auth = request.form

        if not auth or not auth.get('email') or not auth.get('password'):
            return AuthenticationException('Login email and password are required !!')

        user = User.get_user_by_email(auth.get('email'))

        if not user:
            raise AuthenticationException('User does not exist !!')

        if not check_password_hash(user.password, auth.get('password')):
            return AuthenticationException('Wrong Password !!', 403)

        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, app.config['SECRET_KEY'])
        self.response.append_data("user", user.to_dict())
        self.response.append_data("token", token)
        self.response.code = 201
        return self.response.build()
