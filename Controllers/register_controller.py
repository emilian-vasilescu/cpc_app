from flask import request
from Controllers.base_controller import BaseController
from Services.collection_service import CollectionService
from Services.user_service import UserService
from app import db


class RegisterController(BaseController):
    def post(self):
        try:
            user_service = UserService()
            user_service.data = request.form
            user_service.create_user()
        except Exception as e:
            raise e

        db.session.add(user_service.user)
        db.session.commit()

        collection_service = CollectionService(user_service.user)
        collection_service.generate_collection()
        self.response.message = "Successfully registered."
        self.response.append_data("user", user_service.user.to_dict())
        self.response.code = 201
        return self.response.build()
