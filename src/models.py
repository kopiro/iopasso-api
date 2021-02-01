from sqlalchemy_serializer import SerializerMixin
from common import db


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_only = ('id', 'name', 'email')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    birth_date = db.Column(db.String(10))


class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'
    serialize_only = ('id', 'name', 'address')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(250))
    # guests = db.Column(db.String(250))
