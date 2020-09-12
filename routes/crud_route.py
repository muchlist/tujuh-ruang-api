from bson.objectid import ObjectId
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from dao import crud_dao
from input_schemas.crud_input import (CrudSchemaCreate)

bp = Blueprint('crud_bp', __name__, url_prefix='/api')


"""
------------------------------------------------------------------------------
List crud localhost:5001/crud?nama=
------------------------------------------------------------------------------
"""


@bp.route("/crud", methods=['GET', 'POST'])
def find_crud():

    if request.method == 'POST':

        schema = CrudSchemaCreate()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {"msg": str(err.messages)}, 400

        result = crud_dao.create(nama=data["nama"],
                                 alamat=data["alamat"],
                                 keterangan=data["keterangan"])

        return {"msg": f"crud {result} berhasil dibuat"}, 201

    if request.method == 'GET':
        nama = request.args.get("nama")
        crud = crud_dao.find_retrieve(nama)

        return {"crud": crud}, 200


"""
------------------------------------------------------------------------------
Detail crud localhost:5001/crud/objectID
------------------------------------------------------------------------------
"""


@bp.route("/crud/<objek_id>", methods=['GET', 'PUT', 'DELETE'])
def detail(objek_id):
    if not ObjectId.is_valid(objek_id):
        return {"msg": "Object ID tidak valid"}, 400

    if request.method == 'GET':

        crud = crud_dao.get_retrieve(objek_id)

        if crud is None:
            return {"msg": "Crud dengan ID tersebut tidak ditemukan"}, 400

        return jsonify(crud), 200

    if request.method == 'PUT':
        schema = CrudSchemaCreate()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {"msg": str(err.messages)}, 400

        result = crud_dao.update(id=objek_id,
                                 nama=data["nama"],
                                 alamat=data["alamat"],
                                 keterangan=data["keterangan"])

        if result is None:
            return {"msg": "Kesalahan pada ID"}, 400

        return jsonify(result), 200

    if request.method == 'DELETE':

        crud_dao.delete(objek_id)
        return {"msg": "crud dihapus"}, 204
