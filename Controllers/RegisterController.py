import uuid
from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from Models.User import User
from Services.CollectionService import CollectionService
from app import db


class RegisterController(Resource):
    def post(self):
        data = request.form

        name, email, role = data.get('name'), data.get('email'), data.get('role')
        password = data.get('password')

        # @todo Validate data
        if not all([name, email, role, password]):
            return {'message': 'Name, role, email and password are mandatory.'}, 400

        user = User.query \
            .filter_by(email=email) \
            .first()
        if not user:
            # database ORM object
            user = User(
                public_id=str(uuid.uuid4()),
                name=name,
                email=email,
                role=role,
                budget=500,
                password=generate_password_hash(password)
            )
            # insert user
            db.session.add(user)
            db.session.commit()

            user_output = {
                'id': user.id,
                'public_id': user.public_id,
                'name': user.name,
                'role': user.role,
                'email': user.email
            }

            collection_service = CollectionService(user)
            collection_service.generate_collection()

            return {'message': 'Successfully registered.', 'data': {'user': user_output}}, 201
        else:
            return {'message': 'User already exists. Please Log in.'}, 202
