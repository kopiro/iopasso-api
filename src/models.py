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


events_guests = db.Table('events_guests',
                         db.Column('event_id', db.Integer, db.ForeignKey(
                             'events.id'), primary_key=True),
                         db.Column('user_id', db.Integer, db.ForeignKey(
                             'users.id'), primary_key=True)
                         )


class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'
    serialize_only = ('id', 'name', 'address', 'owner_id',
                      'owner', 'date', 'guests')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(250))
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id))
    owner = db.relationship(
        "User", backref=db.backref("users", uselist=False))
    date = db.Column(db.Date)
    guests = db.relationship('User', secondary=events_guests, lazy='subquery',
                             backref=db.backref('events', lazy=True))
