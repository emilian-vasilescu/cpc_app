from flask import request
from Controllers.base_controller import BaseController
from Exceptions.exceptions import AccessDeniedException, ValidationFieldsException, NotFoundException
from Models.user import User
from Services.Decorators.check_jwt_token import check_jwt_token
from Services.collection_service import CollectionService
from Services.user_service import UserService
from app import db


class UserController(BaseController):

    @check_jwt_token
    def get(self, current_user, user_id=None):

        # if user is not admin, return his own data
        if current_user.role != User.ADMIN:
            user_id = current_user.id

        users = []
        if type(user_id) is int:
            user = User.get_user_by_id(user_id)
            if user:
                users.append(user)

        else:
            users = User.get_all_users().paginate(page=self.get_current_page(), per_page=self.get_per_page())

        self.response.build_data_by_records(users)
        return self.response.build()

    @check_jwt_token
    def post(self, current_user, user_id=None):
        if current_user.role != User.ADMIN:
            raise AccessDeniedException(role=current_user.role, message='Only Admins can create other users !!')

        try:
            user_service = UserService()
            user_service.data = request.form
            user_service.create_user(current_user=current_user)
        except Exception as e:
            raise e

        db.session.add(user_service.user)
        db.session.commit()

        collection_service = CollectionService(user_service.user)
        collection_service.generate_collection()

        self.response.message = "User created!"
        self.response.append_data("user", user_service.user.to_dict())
        return self.response.build()

    @check_jwt_token
    def put(self, current_user, user_id=None):
        if current_user.role != User.ADMIN:
            raise AccessDeniedException(role=current_user.role, message='Only Admins can modify other users !!')

        if not user_id:
            raise ValidationFieldsException('Provide an user id !!')

        try:
            user = User.get_user_by_id(user_id)
            user_service = UserService()
            user_service.user = user
            user_service.data = request.form
            user_service.update_user()
        except Exception as e:
            raise e

        db.session.commit()
        self.response.message = "User updated"
        self.response.append_data("user", user.to_dict())
        return self.response.build()

    @check_jwt_token
    def delete(self, current_user, user_id=None):
        if current_user.role != User.ADMIN:
            raise AccessDeniedException(role=current_user.role, message='Only Admins can delete users !!')
        if not user_id:
            raise ValidationFieldsException('Provide an user id !!')

        # delete user
        user = User.get_user_by_id(user_id)

        if not user:
            raise NotFoundException('User does not exist')

        user.cards.clear()
        db.session.delete(user)
        db.session.commit()
        self.response.message = "User deleted"
        return self.response.build()
