
from flask import Blueprint, jsonify
from models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

blue = Blueprint('users', __name__)


@blue.route('/me', methods=['GET'])
@jwt_required()
def route_me():
    user_id = get_jwt_identity()
    return jsonify(User.query.get(user_id).to_dict())
