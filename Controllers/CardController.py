from flask import request
from flask_restful import Resource

from Models.Card import Card
from Models.User import User
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

        data = request.form

        skill_level, name, market_value, age = data.get('skill_level'), data.get('name'), data.get(
            'market_value'), data.get('age')

        card = Card.query \
            .filter_by(id=card_id) \
            .first()

        if not card:
            return {'message': 'Card does not exist'}, 404
        else:
            if not any([skill_level, name, market_value, age]):
                return {'message': 'At least one of skill_level, name, market_value or age is mandatory.'}, 400

            # @todo Validate data
            if skill_level:
                card.skill_level = skill_level
            if name:
                card.name = name
            if market_value:
                card.market_value = market_value
            if age:
                card.age = age

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
