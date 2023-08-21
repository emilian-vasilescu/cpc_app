from flask_restful import Api

from Controllers.CardController import CardController
from Controllers.LoginController import LoginController
from Controllers.MyProfileController import MyProfileController
from Controllers.RegisterController import RegisterController
from Controllers.UserController import UserController
from app import app

api = Api(app)

api.add_resource(LoginController, '/login')
api.add_resource(RegisterController, '/register')
api.add_resource(UserController, '/users/<int:user_id>', '/users')
api.add_resource(MyProfileController, '/my_profile', methods=['GET', 'PUT'])

api.add_resource(CardController, '/cards/<int:card_id>', '/cards', '/users/<int:user_id>/cards')

if __name__ == "__main__":
    app.run(debug=True)
