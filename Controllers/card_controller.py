from flask import request
from Controllers.base_controller import BaseController
from Exceptions.user_role_exception import UserRoleException
from Models.card import Card
from Models.user import User
from Services.card_service import CardService
from Services.Decorators.check_jwt_token import check_jwt_token
from app import db


class CardController(BaseController):
    @check_jwt_token
    def get(self, current_user, card_id=None, user_id=None):

        if current_user.role != User.ADMIN:
            raise UserRoleException(User.ADMIN)

        if type(user_id) is int:
            cards = Card.get_user_cards(user_id)
        elif type(card_id) is int:
            cards = Card.get_card_by_id(card_id)
        else:
            cards = Card.get_all_cards()

        cards_per_page = cards.paginate(page=self.get_current_page(), per_page=self.get_per_page())

        return {
            'data': {
                'cards': [card.to_dict() for card in cards_per_page],
                'page': cards_per_page.page,
                'total': cards_per_page.total
            }
        }

    @check_jwt_token
    def post(self, current_user, card_id=None):
        if current_user.role != User.ADMIN:
            raise UserRoleException(User.ADMIN)

        try:
            card_service = CardService()
            card_service.data = request.form
            card_service.create_card()
        except Exception as e:
            return {'message': str(e)}, 400

        db.session.add(card_service.card)
        db.session.commit()

        return {'message': 'Card created', 'data': {'card': card_service.card.to_dict()}}, 201

    @check_jwt_token
    def put(self, current_user, card_id=None):
        if current_user.role != User.ADMIN:
            raise UserRoleException(User.ADMIN)

        if type(card_id) is not int:
            return {'message': 'Provide a card id !!'}, 403

        try:
            card = Card.query \
                .filter_by(id=card_id) \
                .first()

            card_service = CardService()
            card_service.card = card
            card_service.data = request.form
            card_service.update_card()
        except Exception as e:
            return {'message': str(e)}, 400

        db.session.commit()

        return {'message': 'Card updated', 'data': {'card': card.to_dict()}}, 201

    @check_jwt_token
    def delete(self, current_user, card_id=None):
        if current_user.role != User.ADMIN:
            raise UserRoleException(User.ADMIN)
        if type(card_id) is not int:
            return {'message': 'Provide a card id !!'}, 403

        # delete attached cards
        card = Card.query.filter_by(id=card_id).first()

        if not card:
            return {'message': 'Card does not exist'}, 404

        card.users.clear()
        db.session.delete(card)
        db.session.commit()

        return {'message': 'Card deleted'}, 200
