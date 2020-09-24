from databases.db import mongo
from bson import ObjectId


def get_pelanggan(id_objek: str) -> dict:
    pelanggan = mongo.db.pelanggan.find_one(
        {"_id": ObjectId(id_objek)})
    return pelanggan

def get_pelanggan_by_id_pelanggan(pelanggan_id: str) -> dict:
    pelanggan = mongo.db.pelanggan.find_one(
        {"id_pelanggan": pelanggan_id})
    return pelanggan


def daftar_pelanggan(nama: str) -> list:
    find_filter = {
        "aktif" : True,
    }
    if nama:
        find_filter["nama"] = {'$regex': f'.*{nama.upper()}.*'}

    list_pelanggan = []
    result = mongo.db.pelanggan.find(find_filter).sort("nama", 1)
    for pelanggan in result:
        list_pelanggan.append(pelanggan)

    return list_pelanggan
