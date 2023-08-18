from flask_restful import Api

from Controllers.CardController import CardController
from Controllers.LoginController import LoginController
from Controllers.RegisterController import RegisterController
from Controllers.UserController import UserController
from app import app

api = Api(app)

api.add_resource(LoginController, '/login')
api.add_resource(RegisterController, '/register')
api.add_resource(UserController, '/user/<int:user_id>', '/user')
api.add_resource(CardController, '/card/<int:card_id>', '/card')

if __name__ == "__main__":
    app.run(debug=True)
