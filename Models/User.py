from sqlalchemy_serializer import SerializerMixin

from Models.link_tables import user_card_association
from app import db


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    # https://github.com/n0nSmoker/SQLAlchemy-serializer
    serialize_rules = ('-cards.users', '-password',)

    ADMIN = 'admin'
    USER = 'user'
    INITIAL_BUDGET = 500
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(250), unique=True)
    name = db.Column(db.String(250))
    role = db.Column(db.String(250))
    email = db.Column(db.String(250), unique=True)
    budget = db.Column(db.Float)
    country = db.Column(db.String(250))
    password = db.Column(db.String(250))
    cards = db.relationship('Card', secondary=user_card_association, back_populates='users', lazy=True)

    def __init__(self, public_id, name, role, email, budget, country, password):
        self.public_id = public_id
        self.name = name
        self.role = role
        self.email = email
        self.budget = budget
        self.country = country
        self.password = password

