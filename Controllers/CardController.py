from flask import request
from flask_restful import Resource

from Models.Card import Card
from Models.User import User
from Services.CardService import CardService
from Services.Decorators.check_jwt_token import check_jwt_token
from app import db


class CardController(Resource):
    @check_jwt_token
    def get(self, current_user, card_id=None, user_id=None):

        if type(user_id) is int:
            cards = Card.query.join(Card.users).filter(User.id == user_id).all()
        elif type(card_id) is int:
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

    @check_jwt_token
    def put(self, current_user, card_id=None):
        if current_user.role != User.ADMIN:
            return {'message': 'Only Admins can modify other cards !!'}, 403

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
            return {'message': 'Only Admins can delete cards !!'}, 403
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
