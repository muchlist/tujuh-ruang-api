from flask import Blueprint, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
)
from marshmallow import ValidationError

from dao import (user_query,
                 user_update)
from dto.user_dto import UserDto
from input_schemas.user_input import (UserRegisterSchema,
                                      UserEditSchema)
from utils.my_bcrypt import bcrypt
from validations import role_validations as valid

bp = Blueprint('user_admin_bp', __name__, url_prefix='/admin')


def user_eksis(email):
    if user_query.get_one_without_password(email):
        return True
    return False


"""
------------------------------------------------------------------------------
register
------------------------------------------------------------------------------
"""


@bp.route('/register', methods=['POST'])
# @jwt_required
def register_user():
    # if not valid.is_admin(get_jwt_claims()):
    #     return {"msg": "user tidak memiliki authorisasi"}, 403

    schema = UserRegisterSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400
        # return {"msg": "Input tidak valid"}, 400

    # hash password
    pw_hash = bcrypt.generate_password_hash(
        data["password"]).decode("utf-8")
    data["password"] = pw_hash

    # mengecek apakah user exist
    if user_eksis(data["email"]):
        return {"msg": "user tidak tersedia"}, 400

    # mendaftarkan ke mongodb
    user_dto = UserDto(data['email'],
                       pw_hash, data['name'],
                       data['is_admin'],
                       data['is_staff'],
                       data['is_customer'],
                       data['phone'],
                       data['address'],
                       )
    # try:
    #     user_update.insert_user(user_dto)
    # except:
    #     return {"message": "gagal menyimpan ke database"}, 500
    user_update.insert_user(user_dto)
    return {"msg": "data berhasil disimpan"}, 201


"""
------------------------------------------------------------------------------
Merubah dan mendelete user
------------------------------------------------------------------------------
"""


@bp.route('/users/<string:email>', methods=['PUT', 'DELETE'])
@jwt_required
def put_delete_user(email):
    if not valid.is_admin(get_jwt_claims()):
        return {"msg": "user tidak memiliki authorisasi"}, 400

    if request.method == 'PUT':
        schema = UserEditSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
            # return {"msg": "Input tidak valid"}, 400

        if not user_eksis(email):
            return {"msg": f"user {email} tidak ditemukan"}, 400

        user_dto = UserDto(
            email,
            "", data['name'],
            data['is_admin'],
            data['is_staff'],
            data['is_customer'],
            data['phone'],
            data['address'],
        )

        try:
            user_update.update_user(user_dto)
        except:
            return {"msg": "gagal menyimpan ke database"}, 500

        return {"msg": f"user {email} berhasil diubah"}, 201

    if request.method == 'DELETE':
        if not user_eksis(email):
            return {"msg": f"user {email} tidak ditemukan"}

        user_update.delete_user(email)
        return {"msg": f"user {email} berhasil dihapus"}, 201


"""
------------------------------------------------------------------------------
Reset Password
------------------------------------------------------------------------------
"""


@bp.route('/reset/<string:email>', methods=['GET'])
@jwt_required
def reset_password_by_admin(email):
    if not valid.is_admin(get_jwt_claims()):
        return {"msg": "user tidak memiliki authorisasi"}, 403

    if request.method == 'GET':
        if not user_eksis(email):
            return {"msg": f"user {email} tidak ditemukan"}, 404

        # hash password
        pw_hash = bcrypt.generate_password_hash("Pelindo3").decode("utf-8")

        user_update.put_password(email, pw_hash)

        return {"msg": f"Password user {email} berhasil direset"}, 201
