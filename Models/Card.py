from sqlalchemy_serializer import SerializerMixin
from app import db


class Card(db.Model, SerializerMixin):
    __tablename__ = 'cards'
    serialize_rules = ('-user.cards',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    age = db.Column(db.Integer)
    skill_level = db.Column(db.Float)
    market_value = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship('User', back_populates='cards', lazy=True)

    def __init__(self, name, age, skill_level, market_value, user_id):
        self.name = name
        self.age = age
        self.skill_level = skill_level
        self.market_value = market_value
        self.user_id = user_id
