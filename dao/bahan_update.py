from dto.bahan_dto import EditBahanDto, BahanDto
from databases.db import mongo
from bson.objectid import ObjectId


def buat_bahan(data: BahanDto) -> str:
    data_insert = {
        "nama": data.nama.upper(),
        "harga": data.harga,
        "satuan": data.satuan,
        "punya_dimensi": data.punya_dimensi,
        "diupdate": data.diupdate,
        "diupdate_oleh": data.diupdate_oleh,
        "spek": data.spek,
        "image": data.image,
    }

    return mongo.db.bahan.insert_one(data_insert).inserted_id


def ubah_bahan(data: EditBahanDto) -> dict:

    find = {"_id": ObjectId(data.filter_id),
            "diupdate": data.filter_timestamp}

    update = {
        "nama": data.nama.upper(),
        "harga": data.harga,
        "satuan": data.satuan,
        "punya_dimensi": data.punya_dimensi,
        "diupdate": data.diupdate,
        "diupdate_oleh": data.diupdate_oleh,
        "spek": data.spek,
    }

    return mongo.db.bahan.find_one_and_update(find, {'$set': update}, return_document=True)


def delete_bahan(id_bahan: str):
    mongo.db.bahan.remove({"_id": ObjectId(id_bahan)})
