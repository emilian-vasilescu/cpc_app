from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from Models.User import User
from Services.Decorators.check_jwt_token import check_jwt_token
from app import db


class MyProfileController(Resource):
    @check_jwt_token
    def get(self, current_user):
        return {
            'data': {
                'users': [current_user.to_dict()]
            }
        }

    @check_jwt_token
    def put(self, current_user):
        data = request.form

        name, country = data.get('name'), data.get('country')
        password = data.get('password')

        user = User.query \
            .filter_by(id=current_user.id) \
            .first()

        if not any([name, country, password]):
            return {'message': 'At least one of Name, country or password is mandatory.'}, 400

        # @todo Validate data
        if name:
            user.name = name
        if country:
            user.country = country
        if password:
            user.password = generate_password_hash(password)

        db.session.commit()

        return {'message': 'Profile updated', 'data': {'user': user.to_dict()}}, 201

