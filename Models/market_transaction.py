from datetime import datetime
# from Models.user import User
# from Models.card import Card
from sqlalchemy_serializer import SerializerMixin
from app import db


class MarketTransaction(db.Model, SerializerMixin):
    __tablename__ = 'market_transactions'
    ON_SELL = 'on_sell'
    CANCELED = 'canceled'
    SOLD = 'sold'

    # https://github.com/n0nSmoker/SQLAlchemy-serializer
    serialize_rules = ('-seller', '-buyer', '-card.transactions')

    id = db.Column(db.Integer, primary_key=True)
    asked_value = db.Column(db.Float)
    market_value = db.Column(db.Float)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.String(250), default=ON_SELL)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    modified_at = db.Column(db.DateTime, default=datetime.now())

    seller = db.relationship('User', back_populates='sell_transactions', lazy=True, foreign_keys=[seller_id])
    buyer = db.relationship('User', back_populates='buy_transactions', lazy=True, foreign_keys=[buyer_id])
    card = db.relationship('Card', back_populates='transactions', lazy=True, foreign_keys=[card_id])

    def __init__(self, asked_value, market_value, seller_id, card_id, status=None, buyer_id=None, closed_at=None, modified_at=None):
        self.asked_value = asked_value
        self.market_value = market_value
        self.seller_id = seller_id
        self.card_id = card_id
        self.status = status
        self.buyer_id = buyer_id
        self.closed_at = closed_at
        self.modified_at = modified_at

    @staticmethod
    def get_transaction_by_id(transaction_id):
        return MarketTransaction.query.get(transaction_id)

    @staticmethod
    def get_all_transactions():
        return MarketTransaction.query

    @staticmethod
    def get_transactions_by_status(status):
        return MarketTransaction.query \
            .filter_by(status=status)

    @staticmethod
    def get_on_sell_transaction_for_seller_and_card(seller_id, card_id):
        return MarketTransaction.query \
            .filter_by(card_id=card_id, seller_id=seller_id, status=MarketTransaction.ON_SELL) \
            .first()

    @staticmethod
    def get_number_of_sold_transactions_for_card(card_id):
        return MarketTransaction.query.filter_by(card_id=card_id, status=MarketTransaction.SOLD).count()
