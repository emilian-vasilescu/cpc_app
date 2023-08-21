from sqlalchemy_serializer import SerializerMixin

from Models.link_tables import user_card_association
from app import db


class Card(db.Model, SerializerMixin):
    INITIAL_MARKET_VALUE = 100
    __tablename__ = 'cards'
    serialize_rules = ('-users',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    age = db.Column(db.Integer)
    skill_level = db.Column(db.Float)
    market_value = db.Column(db.Float)
    users = db.relationship('User', secondary=user_card_association, back_populates='cards', lazy=True)

    def __init__(self, name, age, skill_level, market_value):
        self.name = name
        self.age = age
        self.skill_level = skill_level
        self.market_value = market_value
