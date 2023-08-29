from flask import request
from Controllers.base_controller import BaseController
from Models.user import User
from Services.collection_service import CollectionService
from Services.user_service import UserService
from app import db


class RegisterController(BaseController):
    def post(self):
        try:
            user = User.query \
                .filter_by(email=request.form.get('email')) \
                .first()

            if not user:
                user_service = UserService()
                user_service.data = request.form
                user_service.create_user()
            else:
                raise Exception('User already exists. Please Log in.')

        except Exception as e:
            return str(e), 400

        db.session.add(user_service.user)
        db.session.commit()

        collection_service = CollectionService(user_service.user)
        collection_service.generate_collection()

        return {'message': 'Successfully registered.', 'data': {'user': user_service.user.to_dict()}}, 201
