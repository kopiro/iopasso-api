from flask import Blueprint, jsonify, request
from forms import EventForm
from models import db, User, Event
from flask_jwt_extended import jwt_required, get_jwt_identity

blue = Blueprint('events', __name__)


@blue.route('', methods=['POST'])
@jwt_required()
def route_create_event():
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

    return jsonify(event.id)


@blue.route('', methods=['GET'])
@jwt_required()
def route_events_read():
    page = request.args.get('page', 0, type=int)
    limit = request.args.get('limit', 10, type=int)
    total = Event.query.count()
    events = Event.query.offset(page*limit).limit(limit).all()
    base_attrs = ('id', 'name', 'owner_id', 'address', 'datetime')

    data = [event.to_dict(only=base_attrs) for event in events]

    return jsonify({
        'limit': limit,
        'page': page,
        'total': total,
        'data': data
    })


@blue.route('/<id>', methods=['GET'])
@jwt_required()
def route_event_read(id):
    event = Event.query.get_or_404(id)
    return jsonify(event.to_dict())


@blue.route('/<id>', methods=['PUT'])
@jwt_required()
def route_event_edit(id):
    event = Event.query.get_or_404(id)

    form = EventForm(request.form, obj=event)
    if form.validate() == False:
        return jsonify({
            'error': True,
            'message': "Validation failed",
            'validations': list(form.errors.items())
        }), 400

    for name in form.data:
        if name == 'guests':
            event.guests = [User.query.get(id)
                            for id in request.form.getlist('guests')]
        else:
            setattr(event, name, form.data[name])

    db.session.commit()

    return jsonify(True)


@blue.route('/<id>', methods=['DELETE'])
@jwt_required()
def route_event_delete(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()

    return jsonify(True)
