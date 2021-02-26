from flask import Blueprint, jsonify
from models import User
from flask_jwt_extended import jwt_required

blue = Blueprint('guests', __name__)


@blue.route('', methods=['GET'])
@jwt_required()
def guests_collection_get():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])
