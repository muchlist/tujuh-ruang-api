from datetime import datetime, timedelta
import string
import random
from utils.name_generator import create_random_name

from flask_jwt_extended.utils import get_jwt_identity

from bson.objectid import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
)
from marshmallow import ValidationError

from dao import (pesanan_query,
                 pesanan_update,
                 bahan_query,
                 pelanggan_query)
from dto.pesanan_dto import LunasPesananDto, PesananDto, EditPesananDto
from input_schemas.pesanan_input import (BuatPesananSchema, EditPesananSchema, ReportsPesananSchema)
from validations.role_validations import is_admin, is_staff
from utils.reports.pdf_penjualan import generate_pdf

bp = Blueprint('pesanan_bp', __name__, url_prefix='/api')


"""
------------------------------------------------------------------------------
List pesanan localhost:5001/pesanan?nama=lunas=1
------------------------------------------------------------------------------
"""


@bp.route("/pesanan", methods=['GET', 'POST'])
@jwt_required
def find_pesanan():
    claims = get_jwt_claims()

    if request.method == 'POST':

        schema = BuatPesananSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {"msg": str(err.messages)}, 400

        if not is_staff(claims):
            return {"msg": "User tidak memiliki hak akses"}, 400

        # cek apakah id pesanan sudah ada
        timenow = datetime.now()
        hours = 8
        hours_added = datetime.timedelta(hours = hours)

        timenow = timenow + hours_added

        id_pesanan_generate = pesanan_query.pesanan_count() + 1
        currentDay = timenow.now().day
        currentMonth = timenow.now().month
        currentYear = timenow.now().year
        random_char = random.choice(string.ascii_letters)
        id_pesanan_generate = f"{currentDay}{random_char}{currentMonth}{currentYear}-{id_pesanan_generate}"

        # relasi bahan
        id_bahan = data["id_bahan"]
        bahan = bahan_query.get_bahan(id_bahan)
        if bahan is None:
            return {"msg": "Bahan tidak ditemukan"}, 400
        harga_bahan = bahan["harga"]
        total_bayar = harga_bahan * \
            data["ukuran_x"] * data["ukuran_y"] * data["qty"]
        uang_muka = data["uang_muka"]
        sisa_bayar = total_bayar - uang_muka

        if sisa_bayar < 0:
            return {"msg": "Gagal menyimpan, kelebihan bayar"}, 400

        # relasi pelanggan
        id_pelanggan = data["id_pelanggan"]
        pelanggan = pelanggan_query.get_pelanggan_by_id_pelanggan(id_pelanggan)
        if pelanggan is None:
            return {"msg": "Pelanggan tidak ditemukan"}, 400

        pesanan_dto = PesananDto(
            no_transaksi=id_pesanan_generate,
            nama_pesanan=data["nama_pesanan"],
            nama_file=data["nama_file"],
            ukuran_x=data["ukuran_x"],
            ukuran_y=data["ukuran_y"],
            qty=data["qty"],
            total_bayar=total_bayar,
            uang_muka=uang_muka,
            sisa_bayar=sisa_bayar,
            apakah_lunas=data["apakah_lunas"],
            petugas=claims["name"],
            id_petugas=get_jwt_identity(),
            finishing=data["finishing"],
            bahan=bahan["nama"],
            id_bahan=data["id_bahan"],
            harga_bahan=bahan["harga"],
            pelanggan=pelanggan["nama"],
            id_pelanggan=data["id_pelanggan"],
            dibuat=timenow,
            dibuat_oleh=claims["name"],
            diupdate=timenow,
            diupdate_oleh=claims["name"],
            satuan_bahan=bahan["satuan"],
        )

        try:
            pesanan_update.buat_pesanan(pesanan_dto)
        except:
            return {"msg": "Gagal menyimpan data ke database"}, 500

        return {"msg": f"pesanan {id_pesanan_generate} berhasil dibuat"}, 201

    if request.method == 'GET':
        nama = request.args.get("nama")
        lunas = request.args.get("lunas")
        id_pelanggan = request.args.get("pelanggan")
        id_bahan = request.args.get("bahan")

        pesanan = pesanan_query.daftar_pesanan(
            id_pelanggan,
            id_bahan,
            nama,
            lunas,
            None, 
            None)

        return {"pesanan": pesanan}, 200


"""
------------------------------------------------------------------------------
Detail pesanan localhost:5001/pesanan/objectID
------------------------------------------------------------------------------
"""


@bp.route("/pesanan/<id_pesanan>", methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def detail_pesanan(id_pesanan):

    claims = get_jwt_claims()

    if request.method == 'GET':

        try:
            pesanan = pesanan_query.get_pesanan(id_pesanan)
        except:
            return {"msg": "Gagal mengambil data dari database"}, 500

        if pesanan is None:
            return {"msg": "Pesanan dengan ID tersebut tidak ditemukan"}, 400

        return jsonify(pesanan), 200

    if request.method == 'PUT':
        schema = EditPesananSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {"msg": str(err.messages)}, 400

        if not is_staff(claims):
            return {"msg": "User tidak memiliki hak akses"}, 400

        # relasi bahan
        id_bahan = data["id_bahan"]
        bahan = bahan_query.get_bahan(id_bahan)
        if bahan is None:
            return {"msg": "Bahan tidak ditemukan"}, 400
        harga_bahan = bahan["harga"]
        total_bayar = harga_bahan * \
            data["ukuran_x"] * data["ukuran_y"] * data["qty"]
        uang_muka = data["uang_muka"]
        sisa_bayar = total_bayar - uang_muka

        if sisa_bayar < 0:
            return {"msg": "Gagal menyimpan, kelebihan bayar"}, 400

        # relasi pelanggan
        id_pelanggan = data["id_pelanggan"]
        pelanggan = pelanggan_query.get_pelanggan_by_id_pelanggan(id_pelanggan)
        if pelanggan is None:
            return {"msg": "Pelanggan tidak ditemukan"}, 400

        timenow = datetime.now()
        hours = 8
        hours_added = datetime.timedelta(hours = hours)

        timenow = timenow + hours_added

        edit_pesanan_dto = EditPesananDto(
            filter_id=id_pesanan,
            filter_timestamp=data["timestamp_filter"],
            nama_pesanan=data["nama_pesanan"],
            nama_file=data["nama_file"],
            ukuran_x=data["ukuran_x"],
            ukuran_y=data["ukuran_y"],
            qty=data["qty"],
            total_bayar=total_bayar,
            uang_muka=uang_muka,
            sisa_bayar=sisa_bayar,
            apakah_lunas=data["apakah_lunas"],
            petugas=claims["name"],
            id_petugas=get_jwt_identity(),
            finishing=data["finishing"],
            bahan=bahan["nama"],
            id_bahan=data["id_bahan"],
            harga_bahan=bahan["harga"],
            pelanggan=pelanggan["nama"],
            id_pelanggan=data["id_pelanggan"],
            diupdate=timenow,
            diupdate_oleh=claims["name"],
            satuan_bahan=bahan["satuan"],
        )

        try:
            result = pesanan_update.ubah_pesanan(edit_pesanan_dto)
        except AttributeError as err:
            return {"msg": str(err)}, 500

        if result is None:
            return {"msg": "Kesalahan pada ID, atau sudah ada perubahan sebelumnya"}, 400

        return jsonify(result), 200

    if request.method == 'DELETE':
        if not is_admin(claims):
            return {"msg": "User tidak memiliki hak akses"}, 400

        pesanan_update.delete_pesanan(id_pesanan)
        return {"msg": "pesanan dihapus"}, 204


"""
------------------------------------------------------------------------------
melunaskan pesanan localhost:5001/pesanan/no_transaksi/lunas
------------------------------------------------------------------------------
"""


@bp.route("/pesanan/<id_transaksi>/lunas", methods=['GET'])
@jwt_required
def melunasi_pesanan(id_transaksi):

    claims = get_jwt_claims()
    if not is_staff(claims):
        return {"msg": "User tidak memiliki hak akses"}, 400

    timenow = datetime.now()
    hours = 8
    hours_added = datetime.timedelta(hours = hours)

    timenow = timenow + hours_added
    

    lunas_pesanan_dto = LunasPesananDto(filter_id=id_transaksi,
                                        diupdate=timenow,
                                        diupdate_oleh=claims["name"],
                                        id_petugas=get_jwt_identity()
                                        )

    result = pesanan_update.lunasi(lunas_pesanan_dto)
    if result is None:
        return {"msg": "Kesalahan pada ID, atau sudah ada perubahan sebelumnya"}, 400

    return jsonify(result), 200


"""
------------------------------------------------------------------------------
Pesanan Reports
------------------------------------------------------------------------------
"""


@bp.route("/pesanan-reports", methods=['POST'])
@jwt_required
def reports_pesanan():
    claims = get_jwt_claims()

    if request.method == 'POST':

        schema = ReportsPesananSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {"msg": str(err.messages)}, 400

        if not is_staff(claims):
            return {"msg": "User tidak memiliki hak akses"}, 400

        nama = request.args.get("nama")
        lunas = request.args.get("lunas")
        id_pelanggan = request.args.get("pelanggan")
        id_bahan = request.args.get("bahan")

        if lunas == "1":
            title = "Data Penjualan"
        elif lunas == "0":
            title = "Data Piutang"
        else:
            title = "Data Keseluruhan Penjualan (Termasuk yang belum lunas)"

        pdf_file_name = create_random_name()

        pesanan = pesanan_query.daftar_pesanan(
            id_pelanggan,
            id_bahan,
            nama,
            lunas,
            data["start_date"], 
            data["end_date"],)

        if len(pesanan) == 0:
            return {"msg": "Penjualan pada range tanggal tersebut tidak ada"}, 404

        pesanan.reverse()

        generate_pdf(pdf_file_name,pesanan,data["start_date"], data["end_date"], title)

        return {"msg": pdf_file_name}, 200

