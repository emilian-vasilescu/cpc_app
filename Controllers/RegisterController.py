from flask import request
from flask_restful import Resource
from Services.CollectionService import CollectionService
from Services.UserService import UserService
from app import db


class RegisterController(Resource):
    def post(self):
        try:
            user_service = UserService()
            user_service.data = request.form
            user_service.create_user()
        except Exception as e:
            return str(e), 400

        db.session.add(user_service.user)
        db.session.commit()

        collection_service = CollectionService(user_service.user)
        collection_service.generate_collection()

        return {'message': 'Successfully registered.', 'data': {'user': user_service.user.to_dict()}}, 201
