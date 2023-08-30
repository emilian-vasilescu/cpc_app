from sqlalchemy_serializer import SerializerMixin
from Models.user import User
# from Models.market_transaction import MarketTransaction
from Models.user_card import user_card_association

from app import db


class Card(db.Model, SerializerMixin):
    INITIAL_MARKET_VALUE = 100
    __tablename__ = 'cards'
    serialize_rules = ('-users', '-transactions.card')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    age = db.Column(db.Integer)
    skill_level = db.Column(db.Float)
    market_value = db.Column(db.Float)

    users = db.relationship('User', secondary=user_card_association, back_populates='cards', lazy=True)
    transactions = db.relationship('MarketTransaction', back_populates='card', lazy=True)

    def __init__(self, name, age, skill_level, market_value):
        self.name = name
        self.age = age
        self.skill_level = skill_level
        self.market_value = market_value

    @staticmethod
    def get_user_cards(user_id):
        return Card.query.join(Card.users).filter(User.id == user_id)

    @staticmethod
    def get_card_by_id(card_id):
        return Card.query.filter_by(id=card_id)

    @staticmethod
    def get_all_cards():
        return Card.query
