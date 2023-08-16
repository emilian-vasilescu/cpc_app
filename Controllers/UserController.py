import uuid

from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from Models.User import User
from Services.Decorators.check_jwt_token import check_jwt_token
from app import db


class UserController(Resource):

    @check_jwt_token
    def get(self, current_user, user_id=None):

        if type(user_id) is int:
            users = [User.query.get(user_id)]
        else:
            users = User.query.all()

        output = []
        for user in users:
            output.append({
                'id': user.id,
                'public_id': user.public_id,
                'name': user.name,
                'role': user.role,
                'email': user.email
            })

        return {
            'data': {
                'users': output
            }
        }

    @check_jwt_token
    def post(self, current_user, user_id=None):
        # user register exists
        pass
        if current_user.role != User.ADMIN:
            return {'message': 'Only Admins can create users !!'}, 403

    @check_jwt_token
    def put(self, current_user, user_id=None):
        if current_user.role != User.ADMIN:
            return {'message': 'Only Admins can modify users !!'}, 403

        if type(user_id) is not int:
            return {'message': 'Provide an user id !!'}, 403

        data = request.form

        name, email, role = data.get('name'), data.get('email'), data.get('role')
        password = data.get('password')

        user = User.query \
            .filter_by(id=user_id) \
            .first()

        if not user:
            return {'message': 'User does not exist'}, 404
        else:
            if not any([name, email, role, password]):
                return {'message': 'At least one of Name, role, email or password is mandatory.'}, 400

            # @todo Validate data
            if name:
                user.name = name
            if email:
                user.email = email
            if role:
                user.role = role
            if password:
                user.password = generate_password_hash(password)

            db.session.commit()

            user_output = {
                'id': user.id,
                'public_id': user.public_id,
                'name': user.name,
                'role': user.role,
                'email': user.email
            }

            return {'message': 'User updated', 'data': {'user': user_output}}, 201

    @check_jwt_token
    def delete(self, current_user, user_id=None):
        if current_user.role != User.ADMIN:
            return {'message': 'Only Admins can delete users !!'}, 403
        if type(user_id) is not int:
            return {'message': 'Provide an user id !!'}, 403

        user = User.query \
            .filter_by(id=user_id) \
            .first()

        if not user:
            return {'message': 'User does not exist'}, 404

        db.session.delete(user)
        db.session.commit()

        return {'message': 'User deleted'}, 200
