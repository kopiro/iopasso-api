from common import app, db
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity)
from werkzeug.security import generate_password_hash
from forms import LoginForm, RegisterForm, EventForm
from common import app, db
from models import User, Event
from flask import jsonify, request
from werkzeug.security import check_password_hash
from dotenv import load_dotenv

load_dotenv()


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if check_password_hash(user.password, password):
        return user


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

    return jsonify({'success': True, 'user': user.to_dict()}), 200


@app.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate() == False:
        return jsonify({'error': True, 'message': 'Validation failed', 'validations': list(form.errors.items())}), 400

    user = authenticate(form.email.data, form.password.data)
    if not user:
        return jsonify({'error': True, 'message': 'Bad credentials, email or password'}), 401

    return jsonify({
        'access_token': create_access_token(identity=user.id),
        'user': user.to_dict(),
    }), 200


@app.route('/me')
@jwt_required
def me():
    user_id = get_jwt_identity()
    return jsonify(User.query.get(user_id).to_dict())


@app.route('/guests')
@jwt_required
def guests_all():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@app.route('/events', methods=['POST'])
@jwt_required
def events_create():
    form = EventForm(request.form)
    if form.validate() == False:
        return jsonify({'error': True, 'message': "Validation failed", 'validations': list(form.errors.items())}), 400

    event = Event(
        name=form.name.data,
        address=form.address.data,
    )

    db.session.add(event)
    db.session.commit()

    return jsonify({'success': True, 'event': event.to_dict()}), 200


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
