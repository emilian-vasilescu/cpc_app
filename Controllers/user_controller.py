from flask import request
from Controllers.base_controller import BaseController
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
            user = User.query.get(user_id)
            if user:
                users.append(user)

        else:
            users = User.query.paginate(page=self.get_current_page(), per_page=self.get_per_page())

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
            return {'message': 'Only Admins can modify other users !!'}, 400

        if type(user_id) is not int:
            return {'message': 'Provide an user id !!'}, 400

        try:
            user = User.query \
                .filter_by(id=user_id) \
                .first()

            user_service = UserService()
            user_service.user = user
            user_service.data = request.form
            user_service.update_user()
        except Exception as e:
            return {'message': str(e)}, 400

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
