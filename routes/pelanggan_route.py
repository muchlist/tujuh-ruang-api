from datetime import datetime, timedelta
import validations

from bson.objectid import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
)
from marshmallow import ValidationError

from dao import (pelanggan_query,
                 pelanggan_update,)
from dto.pelanggan_dto import PelangganDto, EditPelangganDto
from input_schemas.pelanggan_input import (PelangganRegisterSchema,
                                           PelangganEditSchema,)
from validations.role_validations import is_admin, is_staff
from utils.reports.pdf_pelanggan import generate_pdf
from utils.name_generator import create_random_name

bp = Blueprint('pelanggan_bp', __name__, url_prefix='/api')


"""
------------------------------------------------------------------------------
List pelanggan localhost:5001/pelanggan?nama=
------------------------------------------------------------------------------
"""


@bp.route("/pelanggan", methods=['GET', 'POST'])
@jwt_required
def find_pelanggan():
    claims = get_jwt_claims()

    if request.method == 'POST':

        schema = PelangganRegisterSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {"msg": str(err.messages)}, 400

        if not is_staff(claims):
            return {"msg": "User tidak memiliki hak akses"}, 400

        # cek apakah id pelanggan sudah ada
        pelanggan_eksis = pelanggan_query.get_pelanggan_by_id_pelanggan(
            data["id_pelanggan"])
        if pelanggan_eksis:
            return {"msg": "Pelanggan dengan ID tersebut sudah ada"}, 400

        pelanggan_dto = PelangganDto(id_pelanggan=data["id_pelanggan"],
                                     nama=data["nama"],
                                     email=data["email"],
                                     hp=data["hp"],
                                     alamat=data["alamat"],
                                     total_transaksi_lunas=0,
                                     total_hutang=0,
                                     dibuat=datetime.now(),
                                     diupdate=datetime.now(),
                                     dibuat_oleh=claims["name"],
                                     diupdate_oleh=claims["name"],
                                     aktif=True
                                     )

        try:
            result = pelanggan_update.buat_pelanggan(pelanggan_dto)
        except:
            return {"msg": "Gagal menyimpan data ke database"}, 500

        return {"msg": f"pelanggan {data['id_pelanggan']} berhasil dibuat"}, 201

    if request.method == 'GET':
        nama = request.args.get("nama")
        pelanggan = pelanggan_query.daftar_pelanggan(nama)

        return {"pelanggan": pelanggan}, 200


"""
------------------------------------------------------------------------------
Detail pelanggan localhost:5001/pelanggan/objectID
------------------------------------------------------------------------------
"""


@bp.route("/pelanggan/<objek_id>", methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def detail_pelanggan(objek_id):
    if not ObjectId.is_valid(objek_id):
        return {"msg": "Object ID tidak valid"}, 400

    claims = get_jwt_claims()

    if request.method == 'GET':

        try:
            pelanggan = pelanggan_query.get_pelanggan(objek_id)
        except:
            return {"msg": "Gagal mengambil data dari database"}, 500

        if pelanggan is None:
            return {"msg": "Pelanggan dengan ID tersebut tidak ditemukan"}, 400

        return jsonify(pelanggan), 200

    if request.method == 'PUT':
        schema = PelangganEditSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {"msg": str(err.messages)}, 400

        if not is_staff(claims):
            return {"msg": "User tidak memiliki hak akses"}, 400

        pelanggan_edit_dto = EditPelangganDto(
            filter_id=objek_id,
            filter_timestamp=data["timestamp_filter"],
            nama=data["nama"],
            email=data["email"],
            hp=data["hp"],
            alamat=data["alamat"],
            diupdate=datetime.now(),
            diupdate_oleh=claims["name"],
        )

        try:
            result = pelanggan_update.ubah_pelanggan(pelanggan_edit_dto)
        except AttributeError as err:
            return {"msg": str(err)}, 500

        if result is None:
            return {"msg": "Kesalahan pada ID, atau sudah ada perubahan sebelumnya"}, 400

        return jsonify(result), 200

    if request.method == 'DELETE':
        if not is_admin(claims):
            return {"msg": "User tidak memiliki hak akses"}, 400

        pelanggan_update.nonaktifkan_pelanggan(objek_id)
        return {"msg": "pelanggan dinonaktifkan"}, 204


"""
------------------------------------------------------------------------------
menagktifkan Status pelanggan localhost:5001/pelanggan/objectID/aktif
------------------------------------------------------------------------------
"""


@bp.route("/pelanggan/<objek_id>/aktif", methods=['GET'])
@jwt_required
def mengaktifkan_ulang_pelanggan(objek_id):
    if not ObjectId.is_valid(objek_id):
        return {"msg": "Object ID tidak valid"}, 400

    claims = get_jwt_claims()
    if not is_admin(claims):
        return {"msg": "User tidak memiliki hak akses"}, 400

    pelanggan_update.aktifkan_pelanggan(objek_id)
    return {"msg": "pelanggan diaktifkan"}, 200


"""
Pelanggan report

"""

@bp.route("/pelanggan-reports", methods=['GET', 'POST'])
@jwt_required
def report_pelanggan():
    claims = get_jwt_claims()

    if request.method == 'POST':

        if not is_staff(claims):
            return {"msg": "User tidak memiliki hak akses"}, 400

    
        pelanggan = pelanggan_query.daftar_pelanggan("")

        pdf_file_name = create_random_name()

        # Membuat pdf
        try:
            generate_pdf(pdf_name=pdf_file_name,data_pelanggan=pelanggan)
        except:
            return {"msg": "Membuat PDF Gagal"}, 500

        return {"msg": pdf_file_name}, 200

