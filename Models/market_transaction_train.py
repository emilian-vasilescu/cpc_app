from sqlalchemy_serializer import SerializerMixin
from app import db


class MarketTransactionTrain(db.Model, SerializerMixin):
    __tablename__ = 'market_transactions_train'

    id = db.Column(db.Integer, primary_key=True)
    asked_value = db.Column(db.Float)
    age = db.Column(db.Integer)
    skill_level = db.Column(db.Float)
    market_value = db.Column(db.Float)
    previous_transactions = db.Column(db.Integer)

    def __init__(self, asked_value, age, skill_level, market_value, previous_transactions):
        self.asked_value = asked_value
        self.age = age
        self.skill_level = skill_level
        self.market_value = market_value
        self.previous_transactions = previous_transactions
