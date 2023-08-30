from flask import request
from Controllers.base_controller import BaseController
from Exceptions.exceptions import AccessDeniedException, ValidationFieldsException, NotFoundException
from Models.user import User
from Services.Decorators.check_jwt_token import check_jwt_token
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

        return {
            'data': {
                'users': [user.to_dict() for user in users],
                'page': users.page,
                'total': users.total
            }
        }

    @check_jwt_token
    def put(self, current_user, user_id=None):
        if current_user.role != User.ADMIN:
            raise AccessDeniedException('Only Admins can modify other users !!')

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

        return {'message': 'User updated', 'data': {'user': user.to_dict()}}, 201

    @check_jwt_token
    def delete(self, current_user, user_id=None):
        if current_user.role != User.ADMIN:
            raise AccessDeniedException('Only Admins can delete users !!')
        if not user_id:
            raise ValidationFieldsException('Provide an user id !!')

        # delete user
        user = User.get_user_by_id(user_id)

        if not user:
            raise NotFoundException('User does not exist')

        user.cards.clear()
        db.session.delete(user)
        db.session.commit()

        return {'message': 'User deleted'}, 200
