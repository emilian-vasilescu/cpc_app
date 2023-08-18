from datetime import datetime, timedelta

import jwt
from flask import request, make_response, jsonify
from flask_restful import Resource
from werkzeug.security import check_password_hash

from Models.User import User
from app import app


class LoginController(Resource):
    def post(self):
        auth = request.form

        if not auth or not auth.get('email') or not auth.get('password'):
            return {'message': 'Login email and password are required !!'}, 401

        user = User.query \
            .filter_by(email=auth.get('email')) \
            .first()

        if not user:
            return {'message': 'User does not exist !!'}, 401

        if check_password_hash(user.password, auth.get('password')):
            token = jwt.encode({
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(days=1)
            }, app.config['SECRET_KEY'])

            return {'data': {'token': token, 'user': user.to_dict()}}, 201
        return {'message': 'Wrong Password !!'}, 403
