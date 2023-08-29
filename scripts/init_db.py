from Models.market_transaction import MarketTransaction
from Models.market_transaction_train import MarketTransactionTrain
from Models.user_card import user_card_association
from app import db, app
from Models.card import Card
from Models.user import User


with app.app_context():
    tables = [
        user_card_association,
        MarketTransaction.__table__,
        Card.__table__,
        User.__table__,
        MarketTransactionTrain.__table__
    ]
    # drop all tables

    for table in tables:
        try:
            table.drop(db.engine)
        except Exception as e:
            print(e)

    # create all tables for models
    db.create_all()

