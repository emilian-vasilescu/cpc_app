from flask import request
from Controllers.base_controller import BaseController
from Models.market_transaction import MarketTransaction
from Models.user import User
from Services.Decorators.check_jwt_token import check_jwt_token
from Services.market_transaction_service import MarketTransactionService
from app import db


class MarketTransactionController(BaseController):
    @check_jwt_token
    def get(self, current_user, transaction_id=None):

        transactions = []
        if type(transaction_id) is int:
            transaction = MarketTransaction.get_transaction_by_id(transaction_id)
            if transaction:
                if current_user.role == User.ADMIN or \
                        (current_user.role == User.USER and
                         (current_user.id == transaction.seller_id or current_user.id == transaction.buyer_id)):
                    self.response.append_data("transaction", transaction)

        else:
            if current_user.role == User.ADMIN:
                transactions = MarketTransaction.get_all_transactions()
            else:
                transactions = MarketTransaction.get_visible_transactions_for_user(current_user.id)
            transactions = transactions.paginate(page=self.get_current_page(), per_page=self.get_per_page())
            self.response.build_data_by_records(transactions)

        return self.response.build()

    @check_jwt_token
    def post(self, current_user, transaction_id=None):
        try:
            market_transaction_service = MarketTransactionService()
            market_transaction_service.data = request.form
            market_transaction_service.create_transaction(current_user)
        except Exception as e:
            raise e

        db.session.add(market_transaction_service.transaction)
        db.session.commit()
        self.response.message = "Transaction created"
        self.response.append_data("transaction", market_transaction_service.transaction.to_dict())
        self.response.code = 201
        return self.response.build()

    @check_jwt_token
    def put(self, current_user, transaction_id=None):
        try:
            market_transaction_service = MarketTransactionService()
            market_transaction_service.transaction = MarketTransaction.get_transaction_by_id(transaction_id)
            market_transaction_service.data = request.form
            market_transaction_service.edit_transaction(current_user)
        except Exception as e:
            raise e

        db.session.commit()
        self.response.message = "Transaction updated"
        self.response.append_data("transaction", market_transaction_service.transaction.to_dict())
        return self.response.build()

    @check_jwt_token
    def delete(self, current_user, transaction_id=None):
        try:
            market_transaction_service = MarketTransactionService()
            market_transaction_service.transaction = MarketTransaction.get_transaction_by_id(transaction_id)
            market_transaction_service.data = request.form
            market_transaction_service.delete_transaction(current_user)
        except Exception as e:
            raise e

        db.session.commit()

        self.response.message = "Transaction canceled"
        self.response.append_data("transaction", market_transaction_service.transaction.to_dict())
        return self.response.build()
