from databases.db import mongo
from bson.objectid import ObjectId
from dto.pelanggan_dto import PelangganDto, EditPelangganDto


def buat_pelanggan(data: PelangganDto) -> str:
    data_insert = {
        "id_pelanggan": data.id_pelanggan.upper(),
        "nama": data.nama.upper(),
        "email": data.email.lower(),
        "hp": data.hp,
        "alamat": data.alamat,
        "dibuat": data.dibuat,
        "diupdate": data.diupdate,
        "dibuat_oleh": data.dibuat_oleh,
        "total_transaksi_lunas": 0,
        "total_hutang": 0,
        "aktif": data.aktif
    }

    return mongo.db.pelanggan.insert_one(data_insert).inserted_id


def ubah_pelanggan(data: EditPelangganDto) -> dict:

    find = {"_id": ObjectId(data.filter_id),
            "diupdate": data.filter_timestamp}

    update = {
        "id_pelanggan": data.id_pelanggan.upper(),
        "nama": data.nama,
        "email": data.email.lower(),
        "hp": data.hp,
        "alamat": data.alamat,
    }

    return mongo.db.pelanggan.find_one_and_update(find, {'$set': update}, return_document=True)


def update_transaksi(filter_id: str, lunas: int, hutang: int):
    find = {"_id": ObjectId(filter_id)}
    update = {
        '$inc': {
            "total_transaksi_lunas": lunas,
            "total_hutang": hutang,
        }
    }
    return mongo.db.pelanggan.find_one_and_update(find, update, return_document=True)


def nonaktifkan_pelanggan(filter_id: str):
    find = {"_id": ObjectId(filter_id)}
    update = {
        "aktif": False,
    }

    mongo.db.pelanggan.update_one(find, {'$set': update})


def aktifkan_pelanggan(filter_id: str):
    find = {"_id": ObjectId(filter_id)}
    update = {
        "aktif": True,
    }

    mongo.db.pelanggan.update_one(find, {'$set': update})
