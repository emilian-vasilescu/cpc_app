from flask_restful import Api

from Controllers.card_controller import CardController
from Controllers.login_controller import LoginController
from Controllers.market_transaction_controller import MarketTransactionController
from Controllers.my_profile_controller import MyProfileController
from Controllers.register_controller import RegisterController
from Controllers.user_controller import UserController
from app import app

api = Api(app)

api.add_resource(LoginController, '/login')
api.add_resource(RegisterController, '/register')
api.add_resource(UserController, '/users/<int:user_id>', '/users')
api.add_resource(MyProfileController, '/my_profile', methods=['GET', 'PUT'])

api.add_resource(CardController, '/cards/<int:card_id>', '/cards', '/users/<int:user_id>/cards')
api.add_resource(MarketTransactionController, '/transactions/<int:transaction_id>', '/transactions')

if __name__ == "__main__":
    app.run(debug=True)
