from databases.db import mongo
from bson.objectid import ObjectId


def create(nama: str, alamat: str, keterangan: str) -> str:
    data_insert = {
        "nama": nama.upper(),
        "alamat": alamat,
        "keterangan": keterangan,
    }

    return mongo.db.crud.insert_one(data_insert).inserted_id


def update(id: str, nama: str, alamat: str, keterangan: str) -> dict:

    find = {"_id": ObjectId(id)}

    update = {
        "nama": nama.upper(),
        "alamat": alamat,
        "keterangan": keterangan,
    }

    return mongo.db.crud.find_one_and_update(find, {'$set': update}, return_document=True)


def delete(id: str):
    mongo.db.crud.remove({"_id": ObjectId(id)})


def get_retrieve(id: str) -> dict:
    find = {
        "_id": ObjectId(id)
    }
    return mongo.db.crud.find_one(find)


def find_retrieve(nama: str) -> dict:
    find = {}
    if nama:
        find["nama"] = nama.upper()

    list_crud = []
    result = mongo.db.crud.find(find).sort("_id", -1)
    for crud in result:
        list_crud.append(crud)

    return list_crud
