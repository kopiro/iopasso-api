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
    if not user:
        return None
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
        'id': user.id
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
        return jsonify({
            'error': True,
            'message': "Validation failed",
            'validations': list(form.errors.items())
        }), 400

    user_id = get_jwt_identity()

    event = Event(
        name=form.name.data,
        address=form.address.data,
        datetime=form.datetime.data,
        owner_id=user_id,
        guests=[User.query.get(id) for id in request.form.getlist('guests')]
    )

    db.session.add(event)
    db.session.commit()

    return jsonify({
        'success': True,
        'id': event.id
    }), 200


@app.route('/events', methods=['GET'])
@jwt_required
def events_collection_get():
    page = request.args.get('page', 0, type=int)
    limit = request.args.get('limit', 10, type=int)
    total = Event.query.count()
    events = Event.query.offset(page*limit).limit(limit).all()
    base_attrs = ('id', 'name', 'owner_id', 'address', 'datetime')
    return jsonify({
        'limit': limit,
        'page': page,
        'total': total,
        'data': [event.to_dict(only=base_attrs) for event in events]
    })


@app.route('/events/<id>', methods=['GET'])
@jwt_required
def event_model_get(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({'error': True, 'message': 'Not found'}), 404
    return jsonify(event.to_dict())


@app.route('/events/<id>', methods=['PUT'])
@jwt_required
def event_model_modify(id):
    form = EventForm(request.form)
    if form.validate() == False:
        return jsonify({'error': True, 'message': "Validation failed", 'validations': list(form.errors.items())}), 400

    if request.form.get('id'):
        return jsonify({'error': True, 'message': "ID can't change"}), 400

    num_rows_updated = Event.query.filter_by(id=id).update(request.form)
    db.session.commit()

    return jsonify(num_rows_updated >= 1)


@app.route('/events/<id>', methods=['DELETE'])
@jwt_required
def event_model_delete(id):
    num_rows_updated = Event.query.filter_by(id=id).delete()
    db.session.commit()

    return jsonify(num_rows_updated >= 1)


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
