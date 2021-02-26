from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from libgravatar import Gravatar

db = SQLAlchemy()


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_only = ('id', 'name', 'email', 'image')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    birth_date = db.Column(db.Date, nullable=True)
    registered_on = db.Column(db.DateTime)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    @property
    def image(self):
        return Gravatar(self.email).get_image()


events_guests = db.Table('events_guests',
                         db.Column('event_id', db.Integer, db.ForeignKey(
                             'events.id'), primary_key=True),
                         db.Column('user_id', db.Integer, db.ForeignKey(
                             'users.id'), primary_key=True)
                         )


class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'
    serialize_only = ('id', 'name', 'address', 'owner_id',
                      'owner', 'datetime', 'guests')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(250))
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id))
    owner = db.relationship(
        "User", backref=db.backref("users", uselist=False))
    datetime = db.Column(db.DateTime)
    guests = db.relationship('User', secondary=events_guests, lazy='subquery',
                             backref=db.backref('events', lazy=True))
