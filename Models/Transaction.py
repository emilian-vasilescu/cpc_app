from datetime import datetime

from sqlalchemy_serializer import SerializerMixin
from app import db


class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'

    # https://github.com/n0nSmoker/SQLAlchemy-serializer
    serialize_rules = ('-seller.sell_transactions', '-buyer.buy_transactions', '-card.transactions')

    id = db.Column(db.Integer, primary_key=True)
    asked_value = db.Column(db.Float)
    market_value = db.Column(db.Float)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    closed_at = db.Column(db.DateTime, nullable=True)

    seller = db.relationship('User', back_populates='sell_transactions', lazy=True, foreign_keys=[seller_id])
    buyer = db.relationship('User', back_populates='buy_transactions', lazy=True, foreign_keys=[buyer_id])
    card = db.relationship('Card', back_populates='transactions', lazy=True, foreign_keys=[card_id])

    def __init__(self, asked_value, market_value, seller_id, card_id, buyer_id=None, closed_at=None):
        self.asked_value = asked_value
        self.market_value = market_value
        self.seller_id = seller_id
        self.card_id = card_id
        self.buyer_id = buyer_id
        self.closed_at = closed_at
