from flask import request
from Controllers.base_controller import BaseController
from Exceptions.exceptions import AccessDeniedException, ValidationFieldsException, NotFoundException
from Models.card import Card
from Models.user import User
from Services.card_service import CardService
from Services.Decorators.check_jwt_token import check_jwt_token
from app import db


class CardController(BaseController):
    @check_jwt_token
    def get(self, current_user, card_id=None, user_id=None):

        if current_user.role != User.ADMIN:
            raise AccessDeniedException(role=User.ADMIN)

        if type(user_id) is int:
            cards = Card.query.join(Card.users).filter(User.id == user_id).paginate(page=self.get_current_page(),
                                                                                    per_page=self.get_per_page())
        elif type(card_id) is int:
            cards = Card.query.filter_by(id=card_id).paginate(page=self.get_current_page(),
                                                              per_page=self.get_per_page())
        else:
            cards = Card.query.paginate(page=self.get_current_page(), per_page=self.get_per_page())

        return {
            'data': {
                'cards': [card.to_dict() for card in cards],
                'page': cards.page,
                'total': cards.total
            }
        }

    @check_jwt_token
    def post(self, current_user, card_id=None):
        if current_user.role != User.ADMIN:
            raise AccessDeniedException(role=User.ADMIN)

        try:
            card_service = CardService()
            card_service.data = request.form
            card_service.create_card()
        except Exception as e:
            raise e

        db.session.add(card_service.card)
        db.session.commit()

        return {'message': 'Card created', 'data': {'card': card_service.card.to_dict()}}, 201

    @check_jwt_token
    def put(self, current_user, card_id=None):
        if current_user.role != User.ADMIN:
            raise AccessDeniedException('Only Admins can modify other cards !!')

        if type(card_id) is not int:
            raise ValidationFieldsException('Provide a card id !!')

        try:
            card = Card.query \
                .filter_by(id=card_id) \
                .first()

            card_service = CardService()
            card_service.card = card
            card_service.data = request.form
            card_service.update_card()
        except Exception as e:
            raise e

        db.session.commit()

        return {'message': 'Card updated', 'data': {'card': card.to_dict()}}, 201

    @check_jwt_token
    def delete(self, current_user, card_id=None):
        if current_user.role != User.ADMIN:
            raise AccessDeniedException('Only Admins can delete cards !!')
        if type(card_id) is not int:
            raise ValidationFieldsException('Provide a card id !!')

        # delete attached cards
        card = Card.query.filter_by(id=card_id).first()

        if not card:
            raise NotFoundException('Card does not exist')

        card.users.clear()
        db.session.delete(card)
        db.session.commit()

        return {'message': 'Card deleted'}, 200
