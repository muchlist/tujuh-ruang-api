from databases.db import mongo
from bson import ObjectId


def get_pesanan(no_transaksi: str) -> dict:
    pesanan = mongo.db.pesanan.find_one(
        {"_id": no_transaksi})
    return pesanan


def daftar_pesanan(id_pelanggan: str,
                   id_bahan: str,
                   nama_pelanggan: str,
                   lunas: str) -> list:
    find_filter = {}
    if nama_pelanggan:
        find_filter["pelanggan.nama_pelanggan"] = {
            '$regex': f'.*{nama_pelanggan.upper()}.*'}
    if lunas:
        if lunas == "1":
            find_filter["biaya.apakah_lunas"] = True
        else:
            find_filter["biaya.apakah_lunas"] = False

    if id_pelanggan:
        find_filter["pelanggan.id_pelanggan"] = id_pelanggan
        
    if id_bahan:
        find_filter["bahan.id_bahan"] = id_bahan

    list_pesanan = []
    result = mongo.db.pesanan.find(find_filter).sort("dibuat", -1)
    for pesanan in result:
        list_pesanan.append(pesanan)

    return list_pesanan

def pesanan_count() -> int:
    return mongo.db.pesanan.count_documents({})
