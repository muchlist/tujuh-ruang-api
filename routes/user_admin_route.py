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


def user_eksis(user_id):
    if user_query.get_one_without_password(user_id):
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
        return {"msg": str(err.messages)}, 400

    # hash password
    pw_hash = bcrypt.generate_password_hash(
        data["password"]).decode("utf-8")
    data["password"] = pw_hash

    # mengecek apakah user exist
    if user_eksis(data["user_id"]):
        return {"msg": "user tidak tersedia"}, 400

    # mendaftarkan ke mongodb
    user_dto = UserDto(data['user_id'],
                       pw_hash, data['name'],
                       data['is_admin'],
                       data['is_staff'],
                       data['is_customer'],
                       data['phone'],
                       data['address'],
                       data['join_date'],
                       data['position'],
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


@bp.route('/users/<string:user_id>', methods=['PUT', 'DELETE'])
@jwt_required
def put_delete_user(user_id):
    if not valid.is_admin(get_jwt_claims()):
        return {"msg": "user tidak memiliki authorisasi"}, 400

    if request.method == 'PUT':
        schema = UserEditSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {"msg": str(err.messages)}, 400

        if not user_eksis(user_id):
            return {"msg": f"user {user_id} tidak ditemukan"}, 400

        user_dto = UserDto(
            user_id,
            "", data['name'],
            data['is_admin'],
            data['is_staff'],
            data['is_customer'],
            data['phone'],
            data['address'],
            data['join_date'],
            data['position'],
        )

        try:
            user_update.update_user(user_dto)
        except:
            return {"msg": "gagal menyimpan ke database"}, 500

        return {"msg": f"user {user_id} berhasil diubah"}, 201

    if request.method == 'DELETE':
        if not user_eksis(user_id):
            return {"msg": f"user {user_id} tidak ditemukan"}

        user_update.delete_user(user_id)
        return {"msg": f"user {user_id} berhasil dihapus"}, 201


"""
------------------------------------------------------------------------------
Reset Password
------------------------------------------------------------------------------
"""


@bp.route('/reset/<string:user_id>', methods=['GET'])
@jwt_required
def reset_password_by_admin(user_id):
    if not valid.is_admin(get_jwt_claims()):
        return {"msg": "user tidak memiliki authorisasi"}, 403

    if request.method == 'GET':
        if not user_eksis(user_id):
            return {"msg": f"user {user_id} tidak ditemukan"}, 404

        # hash password
        pw_hash = bcrypt.generate_password_hash("Pelindo3").decode("utf-8")

        user_update.put_password(user_id, pw_hash)

        return {"msg": f"Password user {user_id} berhasil direset"}, 201
