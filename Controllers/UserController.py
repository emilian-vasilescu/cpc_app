from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from Models.Card import Card
from Models.User import User
from Services.Decorators.check_jwt_token import check_jwt_token
from app import db


class UserController(Resource):

    @check_jwt_token
    def get(self, current_user, user_id=None):

        # if user is not admin, return his own data
        if current_user.role != User.ADMIN:
            user_id = current_user.id

        users = []
        if type(user_id) is int:
            user = User.query.get(user_id)
            if user:
                users.append(user)

        else:
            users = User.query.all()

        return {
            'data': {
                'users': [user.to_dict() for user in users]
            }
        }

    @check_jwt_token
    def put(self, current_user, user_id=None):
        if current_user.role != User.ADMIN:
            return {'message': 'Only Admins can modify other users !!'}, 403

        if type(user_id) is not int:
            return {'message': 'Provide an user id !!'}, 403

        data = request.form

        name, email, role, country = data.get('name'), data.get('email'), data.get('role'), data.get('country')
        password = data.get('password')

        user = User.query \
            .filter_by(id=user_id) \
            .first()

        if not user:
            return {'message': 'User does not exist'}, 404
        else:
            if not any([name, email, role, country, password]):
                return {'message': 'At least one of Name, role, email, country or password is mandatory.'}, 400

            # @todo Validate data
            if name:
                user.name = name
            if email:
                user.email = email
            if role:
                user.role = role
            if country:
                user.country = country
            if password:
                user.password = generate_password_hash(password)

            db.session.commit()

            return {'message': 'User updated', 'data': {'user': user.to_dict()}}, 201

    @check_jwt_token
    def delete(self, current_user, user_id=None):
        if current_user.role != User.ADMIN:
            return {'message': 'Only Admins can delete users !!'}, 403
        if type(user_id) is not int:
            return {'message': 'Provide an user id !!'}, 403

        # delete user
        user = User.query \
            .filter_by(id=user_id) \
            .first()

        if not user:
            return {'message': 'User does not exist'}, 404

        user.cards.clear()
        db.session.delete(user)
        db.session.commit()

        return {'message': 'User deleted'}, 200
