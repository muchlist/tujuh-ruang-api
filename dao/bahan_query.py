from databases.db import mongo
from bson import ObjectId


def get_bahan(id_objek: str) -> dict:
    bahan = mongo.db.bahan.find_one(
        {"_id": ObjectId(id_objek)})
    return bahan

def daftar_bahan(nama: str) -> list:
    find_filter = {}
    if nama:
        find_filter["nama"] = {'$regex': f'.*{nama.upper()}.*'}

    list_bahan = []
    result = mongo.db.bahan.find(find_filter).sort("nama", 1)
    for bahan in result:
        list_bahan.append(bahan)

    return list_bahan
