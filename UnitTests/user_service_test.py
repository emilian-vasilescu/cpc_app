import unittest

from Services.user_service import UserService


class UserServiceTest(unittest.TestCase):

    def setUp(self):
        user_service = UserService()
        user_service.data = {
            'name': 'name_test_1',
            'email': 'email_test@gameloft.com',
            'country': 'country_test',
            'role': 'role_admin',
            'password': 'password'
        }
        user_service.create_user()
        self.user = user_service.user

    def test_user_details(self):
        self.assertEqual(self.user.name, 'name_test_2', 'incorrect user name')


if __name__ == "__main__":
    unittest.main()
