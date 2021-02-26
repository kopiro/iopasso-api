from datetime import datetime
from flask import Blueprint, jsonify, request, redirect
from forms import LoginForm, RecoverForm, RegisterForm, ChangePasswordForm
from models import db, User
from flask_jwt_extended import create_access_token
from common import build_www_link, send_email
from itsdangerous import URLSafeTimedSerializer
from os import getenv
from flask.helpers import url_for


blue = Blueprint('auth', __name__)


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None


def get_data_from_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(getenv('SECRET_KEY'))
    try:
        email = serializer.loads(
            token, salt=getenv('SALT_KEY'), max_age=expiration)
    except:
        return False
    return email


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(getenv('SECRET_KEY'))
    return serializer.dumps(email, salt=getenv('SALT_KEY'))


def send_confirmation_email(user):
    token = generate_confirmation_token(user.email)
    confirm_link = url_for("auth.route_confirm_token",
                           token=token, _external=True)
    send_email(user.email,
               "Welcome!", 'To activate your user, click here: <a href="' +
               confirm_link + '">' + confirm_link + '</a>')
    return token, confirm_link


@blue.route('/register', methods=['POST'])
def route_register():
    form = RegisterForm(request.form)
    if form.validate() == False:
        return jsonify({
            'error': True,
            'message': "Validation failed",
            'validations': list(form.errors.items())
        }), 400

    existing_user = User.query.filter_by(email=form.email.data).first()
    if existing_user:
        return jsonify({
            'error': True,
            'message': 'This user already exists'
        }), 400

    user = User(
        name=form.name.data,
        email=form.email.data,
        birth_date=form.birth_date.data,
        registered_on=datetime.now()
    )
    user.set_password(form.password.data)

    send_confirmation_email(user)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'success': True,
        'user': user.to_dict()
    })


@blue.route('/confirm/<token>', methods=['GET'])
def route_confirm_token(token):
    try:
        email = get_data_from_token(token)
    except:
        return redirect(build_www_link("/error.html"))

    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        return redirect(build_www_link("/confirmation-success.html"))

    user.confirmed = True
    user.confirmed_on = datetime.now()

    db.session.commit()

    return redirect(build_www_link("/confirmation-success.html"))


def send_recover_password_email(user):
    token = generate_confirmation_token(user.email)
    recover_link = build_www_link("/change-password.html?token=" + token)
    send_email(user.email,
               "Welcome!", 'To recover your password, click here: <a href="' +
               recover_link + '">' + recover_link + '</a>')
    return token, recover_link


@blue.route('/login', methods=['POST'])
def route_login():
    form = LoginForm(request.form)
    if form.validate() == False:
        return jsonify({
            'error': True,
            'message': 'Validation failed',
            'validations': list(form.errors.items())
        }), 400

    user = authenticate(form.email.data, form.password.data)
    if not user:
        return jsonify({
            'error': True,
            'message': 'Bad credentials, email or password'
        }), 401

    if not user.confirmed:
        send_confirmation_email(user)
        return jsonify({
            'error': True,
            'message': 'User not confirmed, please check your email'
        }), 401

    return jsonify({
        'access_token': create_access_token(identity=user.id),
        'id': user.id
    })


@blue.route('/recover', methods=['POST'])
def route_recover():
    form = RecoverForm(request.form)
    if form.validate() == False:
        return jsonify({
            'error': True,
            'message': 'Validation failed',
            'validations': list(form.errors.items())
        }), 400

    user = User.query.filter_by(email=form.email.data).first()
    if user:
        token, recover_link = send_recover_password_email(user)

    return jsonify({
        'success': True,
        'message': "If the email belongs to a user, an email has been sent to initiate recovery process",
        "__debug__": {'token': token, 'link': recover_link} if getenv('FLASK_ENV') == 'development' else {}
    })


@blue.route('/change-password', methods=['POST'])
def route_change_password():
    form = ChangePasswordForm(request.form)
    if form.validate() == False:
        return jsonify({
            'error': True,
            'message': 'Validation failed',
            'validations': list(form.errors.items())
        }), 400

    try:
        email = get_data_from_token(form.token.data)
    except:
        return jsonify({
            'error': True,
            'message': 'Invalid token',
        }), 400

    user = User.query.filter_by(email=email).first_or_404()
    user.set_password(form.password.data)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Password succesfully changed',
    })
