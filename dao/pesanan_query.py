from databases.db import mongo
from bson import ObjectId


def get_pesanan(no_transaksi: str) -> dict:
    pesanan = mongo.db.pesanan.find_one(
        {"_id": no_transaksi})
    return pesanan

def daftar_pesanan(nama_pelanggan: str, lunas: bool) -> list:
    find_filter = {}
    if nama_pelanggan:
        find_filter["pelanggan.nama_pelanggan"] = {'$regex': f'.*{nama_pelanggan.upper()}.*'}
    if lunas:
        find_filter["biaya.apakah_lunas"] = lunas

    list_pesanan = []
    result = mongo.db.pesanan.find(find_filter).sort("dibuat", -1)
    for pesanan in result:
        list_pesanan.append(pesanan)

    return list_pesanan