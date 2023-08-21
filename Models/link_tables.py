from sqlalchemy import Column, Integer, Table, ForeignKey
from app import db

user_card_association = Table(
    'user_card',
    db.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('card_id', Integer, ForeignKey('cards.id'))
)
