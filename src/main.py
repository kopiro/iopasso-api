from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, StringField, PasswordField, validators
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()


class LoginForm(Form):
    email = StringField("email", validators=[validators.Length(
        min=7, max=50), validators.DataRequired(message="Email is required")])
    password = PasswordField("password", validators=[
                             validators.DataRequired(message="Password is required")])


class RegisterForm(Form):
    name = StringField("name", validators=[validators.Length(
        min=3, max=25), validators.DataRequired(message="Name is required")])
    email = StringField("email", validators=[validators.Length(
        min=3, max=25), validators.DataRequired(message="Email is required")])
    password = PasswordField("password", validators=[
        validators.DataRequired(message="Password is required"),
        validators.EqualTo(fieldname="password_2",
                           message="The password doesn't match")
    ])
    password_2 = PasswordField("password_2", validators=[
        validators.DataRequired(message="Confirm password is required")])
    birth_date = PasswordField("birth_date")


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
app = Flask(__name__)
CORS(app)


db_filename = 'sqlite:///' + os.getcwd() + '/data/db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256))
    birth_date = db.Column(db.String(10))


@app.route('/register', methods=['POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate() == False:
        return jsonify({'error': True, 'message': "Validation failed", 'validations': list(form.errors.items())}), 400

    existing_user = User.query.filter_by(email=form.email.data).first()
    if existing_user:
        return jsonify({'error': True, 'message': 'This user already exists'}), 400

    hashed_password = generate_password_hash(
        form.password.data, method='sha256')
    user = User(
        name=form.name.data,
        email=form.email.data,
        birth_date=form.birth_date.data,
        password=hashed_password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'success': True}), 200


@app.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate() == False:
        return jsonify({'error': True, 'message': 'Validation failed', 'validations': list(form.errors.items())}), 400

    user = User.query.filter_by(email=form.email.data).first()
    if not user:
        return jsonify({'error': True, 'message': 'Bad credentials, email or password'}), 401

    if not check_password_hash(user.password, form.password.data):
        return jsonify({'error': True, 'message': 'Bad credentials, email or password'}), 401

    return jsonify({'id': user.id}), 200


if __name__ == 'main':
    db.create_all()
    app.run(debug=True)
