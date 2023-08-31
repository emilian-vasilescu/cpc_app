from flask import request
from flask_restful import Resource

from Controllers.base_controller import BaseController
from Models.user import User
from Services.Decorators.check_jwt_token import check_jwt_token
from Services.user_service import UserService
from app import db


class MyProfileController(BaseController):
    @check_jwt_token
    def get(self, current_user):
        self.response.append_data("user", current_user.to_dict())
        return self.response.build()

    @check_jwt_token
    def put(self, current_user):

        try:
            user = User.get_user_by_id(current_user.id)
            user_service = UserService()
            user_service.user = user
            user_service.data = request.form
            user_service.update_my_profile()
        except Exception as e:
            raise e

        db.session.commit()
        self.response.message = "Profile updated"
        self.response.append_data("user", user.to_dict())
        self.response.code = 201
        return self.response.build()
