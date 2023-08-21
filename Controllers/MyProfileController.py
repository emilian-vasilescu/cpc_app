from flask import request
from flask_restful import Resource
from Models.User import User
from Services.Decorators.check_jwt_token import check_jwt_token
from Services.UserService import UserService
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

        try:
            user = User.query \
                .filter_by(id=current_user.id) \
                .first()

            user_service = UserService()
            user_service.user = user
            user_service.data = request.form
            user_service.update_my_profile()
        except Exception as e:
            return {'message': str(e)}, 400

        db.session.commit()

        return {'message': 'Profile updated', 'data': {'user': user.to_dict()}}, 201
