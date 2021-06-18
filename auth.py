from flask import Blueprint, jsonify, request

from models import User, sa

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    try:
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        sa.session.add(user)
        sa.session.commit()
        return jsonify({'msg': f'{user.username} is created'}), 201
    except AssertionError as e:
        return jsonify({'msg': f'{e}'}), 400


@auth.route('/login', methods=['POST'])
def login():
    return jsonify({'method': 'login'})
