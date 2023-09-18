import unittest

from Models.user import User
from Models.card import Card
from Services.card_service import CardService
from Services.user_service import UserService
from app import app


class TestCardService(unittest.TestCase):

    def test_card_details(self):
        with app.app_context():
            card_service = CardService()
            card_service.data = {
                'skill_level': 12,
                'name': 'Card Name',
                'market_value': 15,
                'age': 25
            }
            card_service.create_card()
            self.assertEqual(card_service.card.name, 'Card Name', 'correct card name')


if __name__ == "__main__":
    unittest.main()
