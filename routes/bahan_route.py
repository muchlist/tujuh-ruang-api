from datetime import datetime

from bson.objectid import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
)
from marshmallow import ValidationError

from dao import (bahan_query,
                 bahan_update,)
from dto.bahan_dto import BahanDto, EditBahanDto
from input_schemas.bahan_input import (BahanRegisterSchema,
                                       BahanEditSchema,)
from validations.role_validations import is_admin, is_staff

bp = Blueprint('bahan_bp', __name__, url_prefix='/api')


"""
------------------------------------------------------------------------------
List bahan localhost:5001/bahan?nama=
------------------------------------------------------------------------------
"""


@bp.route("/bahan", methods=['GET', 'POST'])
@jwt_required
def find_bahan():
    claims = get_jwt_claims()

    if request.method == 'POST':

        schema = BahanRegisterSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {"msg": str(err.messages)}, 400

        if not is_staff(claims):
            return {"msg": "User tidak memiliki hak akses"}, 400

        bahan_dto = BahanDto(nama=data["nama"],
                             harga=data["harga"],
                             satuan=data["satuan"],
                             punya_dimensi=data["punya_dimensi"],
                             diupdate=datetime.now(),
                             diupdate_oleh=claims["name"],
                             spek=data["spek"],
                             image=""
                             )

        try:
            result = bahan_update.buat_bahan(bahan_dto)
        except:
            return {"msg": "Gagal menyimpan data ke database"}, 500

        return {"msg": f"bahan {result} berhasil dibuat"}, 201

    if request.method == 'GET':
        nama = request.args.get("nama")
        bahan = bahan_query.daftar_bahan(nama)

        return {"bahan": bahan}, 200


"""
------------------------------------------------------------------------------
Detail bahan localhost:5001/bahan/objectID
------------------------------------------------------------------------------
"""


@bp.route("/bahan/<objek_id>", methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def detail_bahan(objek_id):
    if not ObjectId.is_valid(objek_id):
        return {"msg": "Object ID tidak valid"}, 400

    claims = get_jwt_claims()

    if request.method == 'GET':

        try:
            bahan = bahan_query.get_bahan(objek_id)
        except:
            return {"msg": "Gagal mengambil data dari database"}, 500

        if bahan is None:
            return {"msg": "bahan dengan ID tersebut tidak ditemukan"}, 400

        return jsonify(bahan), 200

    if request.method == 'PUT':
        schema = BahanEditSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {"msg": str(err.messages)}, 400

        if not is_staff(claims):
            return {"msg": "User tidak memiliki hak akses"}, 400

        bahan_edit_dto = EditBahanDto(
            filter_id=objek_id,
            filter_timestamp=data["timestamp_filter"],
            nama=data["nama"],
            harga=data["harga"],
            satuan=data["satuan"],
            punya_dimensi=data["punya_dimensi"],
            diupdate=datetime.now(),
            diupdate_oleh=claims["name"],
            spek=data["spek"],
        )

        try:
            result = bahan_update.ubah_bahan(bahan_edit_dto)
        except AttributeError as err:
            return {"msg": str(err)}, 500

        if result is None:
            return {"msg": "Kesalahan pada ID, atau sudah ada perubahan sebelumnya"}, 400

        return jsonify(result), 200

    if request.method == 'DELETE':
        if not is_admin(claims):
            return {"msg": "User tidak memiliki hak akses"}, 400

        bahan_update.delete_bahan(objek_id)
        return {"msg": "bahan dihapus"}, 204
