from flask_restful import Resource

from Models.Card import Card
from Models.User import User
from Services.Decorators.check_jwt_token import check_jwt_token


class CardController(Resource):
    @check_jwt_token
    def get(self, current_user, card_id=None):

        cards = []
        if type(card_id) is int:
            cards = Card.query.filter_by(id=card_id)
        else:
            cards = Card.query.all()

        if current_user.role != User.ADMIN:
            # filter records if is not admin
            cards = [card for card in cards if card.user_id == current_user.id]

        return {
            'data': {
                'cards': [card.to_dict() for card in cards]
            }
        }
