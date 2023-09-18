import unittest

from Models.user import User
from Models.card import Card
from Services.user_service import UserService
from app import app


class TestUserService(unittest.TestCase):

    def test_user_details(self):
        with app.app_context():
            user_service = UserService()
            user_service.data = {
                'name': 'name_test_1',
                'email': 'email_test@gameloft.com',
                'country': 'country_test',
                'role': User.ADMIN,
                'password': 'password'
            }
            user_service.create_user()
            self.assertEqual(user_service.user.name, 'name_test_1', 'correct user name')


if __name__ == "__main__":
    unittest.main()
