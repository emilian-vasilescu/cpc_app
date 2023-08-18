from sqlalchemy_serializer import SerializerMixin
from app import db


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    # https://github.com/n0nSmoker/SQLAlchemy-serializer
    serialize_rules = ('-cards.user', '-password',)

    ADMIN = 'admin'
    USER = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(250), unique=True)
    name = db.Column(db.String(250))
    role = db.Column(db.String(250))
    email = db.Column(db.String(250), unique=True)
    budget = db.Column(db.Float)
    password = db.Column(db.String(250))
    cards = db.relationship('Card', back_populates='user', lazy=True)

    def __init__(self, public_id, name, role, email, budget, password):
        self.public_id = public_id
        self.name = name
        self.role = role
        self.email = email
        self.budget = budget
        self.password = password

