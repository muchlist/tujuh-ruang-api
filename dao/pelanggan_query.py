from databases.db import mongo


def get_pelanggan(id_pelanggan: str) -> dict:
    pelanggan = mongo.db.pelanggan.find_one(
        {"id_pelanggan": id_pelanggan.upper()})
    return pelanggan


def cari_pelanggan_by_nama(nama: str) -> list:
    query_string = {'$regex': f'.*{nama.upper()}.*'}

    koleksi_pelanggan = mongo.db.pelanggan.find(
        {"nama": query_string}
    ).sort("nama", 1)

    list_pelanggan = []

    for pelanggan in koleksi_pelanggan:
        list_pelanggan.append(pelanggan)

    return list_pelanggan


def daftar_pelanggan() -> list:
    list_pelanggan = []
    result = mongo.db.pelanggan.find({}).sort("nama", 1)
    for pelanggan in result:
        list_pelanggan.append(pelanggan)

    return list_pelanggan
