from functools import wraps

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_required, get_jwt_identity, JWTManager, verify_jwt_in_request, get_jwt

from models import User, sa, RoleSchema

auth = Blueprint('auth', __name__)
jwt = JWTManager()


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_admin"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    try:
        user = User.find(data['username'], data['email'])
        if user:
            return jsonify({'msg': f'User {user.username} already exists'}), 400

        user = User(
            username=data['username'],
            email=data['email']
        )
        User.create(user, data['password'])
        return jsonify({'msg': f'{user.username} is created'}), 201
    except AssertionError as e:
        return jsonify({'msg': f'{e}'}), 400


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.find(data['username'], data['email'])

    if not user:
        return jsonify({'msg': 'User not found'}), 404
    elif not user.check_password(data['password']):
        return jsonify({'msg': 'Password incorrect'}), 401

    # roles = RoleSchema().dump(user.roles)
    access_token = create_access_token(
        identity=user.id,
        additional_claims={
            'is_admin': False
            # 'is_admin': any(x.name.upper() == "ADMIN" for x in roles)
        })
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@auth.route("/identity", methods=["GET"])
@jwt_required()
def protected():
    identity = get_jwt_identity()
    return jsonify(identity=identity)


@auth.route('/admin', methods=['GET'])
@admin_required()
def test_admin():
    return jsonify(msg='Admin authorized')
