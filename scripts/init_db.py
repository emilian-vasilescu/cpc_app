from Models.Transaction import Transaction
from Models.link_tables import user_card_association
from app import db, app
from Models.Card import Card
from Models.User import User


with app.app_context():
    tables = [
        user_card_association,
        Transaction.__table__,
        Card.__table__,
        User.__table__,
    ]
    # drop all tables

    for table in tables:
        try:
            table.drop(db.engine)
        except Exception as e:
            print(e)

    # create all tables for models
    db.create_all()

