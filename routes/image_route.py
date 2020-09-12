import os
import time

from bson.objectid import ObjectId
from flask import Blueprint, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
)
from flask_uploads import UploadNotAllowed
from marshmallow import ValidationError

from config import config as cf
from dao import bahan_query, bahan_update
from input_schemas.image_input import ImageSchema
from utils import image_helper
from validations.role_validations import is_staff

# Set up a Blueprint
bp = Blueprint('image_bp', __name__, url_prefix='/api')


@bp.route('/bahan/<id_bahan>/upload', methods=['POST'])
@jwt_required
def upload_stock_image(id_bahan):
    # static/images/namafolder/namafile

    # Input Validation
    schema = ImageSchema()
    try:
        data = schema.load(request.files)
    except ValidationError as err:
        return err.messages, 400

    if not ObjectId.is_valid(id_bahan):
        return {"msg": "Object ID tidak valid"}, 400

    # AUTH
    claims = get_jwt_claims()
    if not is_staff(claims):
        return {"msg": "User tidak memiliki hak akses"}, 400

    # Cek apakah bahan valid
    bahan_object = bahan_query.get_bahan(id_bahan)
    if bahan_object is None:
        return {"msg": "ID bahan tidak tersedia"}, 400
    exist_image = bahan_object["image"]

    # Mendapatkan extensi pada file yang diupload
    extension = image_helper.get_extension(data['image'])

    # Memberikan Nama file dan ekstensi
    file_name = f"{bahan_object['_id']}-{int(time.time())}{extension}"
    folder = "bahan"

    # Menghapus Image existing
    delete_image_existing(exist_image)

    # SAVE IMAGE
    try:
        image_path = image_helper.save_image(
            data['image'], folder=folder, name=file_name)
        # basename = image_helper.get_basename(image_path)  # mengembalikan image.jpg
    except UploadNotAllowed:
        extension = image_helper.get_extension(data['image'])
        return {"msg": f"extensi {extension} not allowed"}, 400

    bahan_updated = bahan_update.ubah_gambar_bahan(bahan_object['_id'], image_path)
    if bahan_updated is None:
        return {"msg": "Gagal menyimpan ke database"}, 400

    return bahan_updated, 200


def delete_image_existing(exist_image: str):
    # Menghapus Image existing
    if exist_image != "":
        try:
            filepath = os.path.join(cf.get('uploaded_image_dest'), exist_image)
            if os.path.exists(filepath):
                os.remove(filepath)
        except:
            return {"msg": "Menghapus image eksisting gagal"}, 500