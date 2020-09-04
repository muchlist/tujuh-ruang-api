from datetime import timedelta

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from marshmallow import ValidationError

from dao import (user_query,
                 user_update)
from input_schemas.user_input import (UserLoginSchema,
                                      UserChangePassSchema)
from utils.my_bcrypt import bcrypt

bp = Blueprint('user_bp', __name__)

EXPIRED_TOKEN = 30

"""
------------------------------------------------------------------------------
login
------------------------------------------------------------------------------
"""


@bp.route('/login', methods=['POST'])
def login_user():
    schema = UserLoginSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400
        # return {"msg": "Input tidak valid"}, 400

    # mendapatkan data user termasuk password
    user = user_query.get_one(data["email"])

    # Cek apakah hash password sama
    if not (user and bcrypt.check_password_hash(user["password"], data["password"])):
        return {"msg": "user atau password salah"}, 400

    # Membuat akses token menggunakan email di database
    access_token = create_access_token(
        identity=user["email"],
        expires_delta=timedelta(days=EXPIRED_TOKEN),
        fresh=True)

    response = {
        'access_token': access_token,
        'email': user['email'],
        'name': user['name'],
        'is_admin': user['is_admin'],
        'is_staff': user['is_staff'],
        "is_customer": user["is_customer"],
    }, 200

    return response


"""
------------------------------------------------------------------------------
Detail user by email
------------------------------------------------------------------------------
"""


@bp.route("/users/<string:email>", methods=['GET'])
@jwt_required
def user(email):
    result = user_query.get_one_without_password(email)
    return jsonify(result), 200


"""
------------------------------------------------------------------------------
Detail user by name
------------------------------------------------------------------------------
"""


@bp.route("/getuser/<name>", methods=['GET'])
@jwt_required
def user_by_name(name):
    users = user_query.get_many_by_name(name)
    return {"users": users}, 200


"""
------------------------------------------------------------------------------
Detail user by self profil
------------------------------------------------------------------------------
"""


@bp.route("/profile", methods=['GET'])
@jwt_required
def show_profile():
    result = user_query.get_one_without_password(get_jwt_identity())
    return jsonify(result), 200


"""
------------------------------------------------------------------------------
List User
------------------------------------------------------------------------------
"""


@bp.route("/users", methods=['GET'])
@jwt_required
def user_list():
    users = user_query.get_many()

    return jsonify(users), 200


"""
------------------------------------------------------------------------------
Self Change Password
------------------------------------------------------------------------------
"""


@bp.route('/change-password', methods=['POST'])
@jwt_required
def change_password():
    schema = UserChangePassSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400
        # return {"msg": "Input tidak valid"}, 400

    user_email = get_jwt_identity()

    user = user_query.get_one(user_email)

    # Cek apakah hash password inputan sama
    if not bcrypt.check_password_hash(user["password"], data["password"]):
        return {'msg': "password salah"}, 400

    # menghash password baru
    new_password_hash = bcrypt.generate_password_hash(
        data["new_password"]).decode("utf-8")

    user_update.put_password(user_email, new_password_hash)
    return {'msg': "password berhasil di ubah"}, 200
