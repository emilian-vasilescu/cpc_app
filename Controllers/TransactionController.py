from flask_restful import Resource

from Services.Decorators.check_jwt_token import check_jwt_token


class TransactionController(Resource):
    @check_jwt_token
    def get(self, current_user, transaction_id=None):
        pass

    @check_jwt_token
    def post(self, current_user, transaction_id=None):
        pass

    @check_jwt_token
    def put(self, current_user, transaction_id=None):
        pass

    @check_jwt_token
    def delete(self, current_user, transaction_id=None):
        pass
