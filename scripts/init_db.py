from Models.link_tables import user_card_association
from app import db, app
from Models.Card import Card
from Models.User import User


with app.app_context():
    # drop all tables
    user_card_association.drop(db.engine)
    Card.__table__.drop(db.engine)
    User.__table__.drop(db.engine)

    # create all tables for models
    db.create_all()

