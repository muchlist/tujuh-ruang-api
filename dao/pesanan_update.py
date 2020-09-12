from dto.pesanan_dto import EditPesananDto, LunasPesananDto, PesananDto
from dto.bahan_dto import EditBahanDto, BahanDto
from databases.db import mongo
from bson.objectid import ObjectId


def buat_pesanan(data: PesananDto) -> str:

    pelanggan_embed = {
        "nama_pelanggan": data.pelanggan.upper(),
        "id_pelanggan": data.id_pelanggan,
    }

    bahan_embed = {
        "nama_bahan": data.bahan,
        "id_bahan": data.id_bahan,
        "harga_bahan": data.harga_bahan,
        "finishing": data.finishing,
        "ukuran_x": data.ukuran_x,
        "ukuran_y": data.ukuran_y,
        "qty": data.qty,
    }

    biaya_embed = {
        "total_bayar": data.total_bayar,
        "uang_muka": data.uang_muka,
        "sisa_bayar": data.sisa_bayar,
        "apakah_lunas": data.apakah_lunas,
    }

    data_insert = {
        "_id": data.no_transaksi,
        "nama_pesanan": data.nama_pesanan,
        "nama_file": data.nama_file,
        "petugas": data.petugas,
        "id_petugas": data.id_petugas,
        "dibuat": data.dibuat,
        "dibuat_oleh": data.dibuat_oleh,
        "diupdate": data.diupdate,
        "diupdate_oleh": data.diupdate_oleh,
        "pelanggan": pelanggan_embed,
        "bahan": bahan_embed,
        "biaya": biaya_embed,
    }

    return mongo.db.pesanan.insert_one(data_insert).inserted_id


def ubah_pesanan(data: EditPesananDto) -> dict:

    find = {"_id": data.filter_id,
            "diupdate": data.filter_timestamp,
            "biaya.apakah_lunas": False
            }

    update = {
        "nama_pesanan": data.nama_pesanan,
        "nama_file": data.nama_file,
        "petugas": data.petugas,
        "id_petugas": data.id_petugas,
        "diupdate": data.diupdate,
        "diupdate_oleh": data.diupdate_oleh,
        "pelanggan.nama_pelanggan":  data.pelanggan.upper(),
        "pelanggan.id_pelanggan":   data.id_pelanggan,
        "bahan.nama_bahan": data.bahan,
        "bahan.id_bahan": data.id_bahan,
        "bahan.harga_bahan": data.harga_bahan,
        "bahan.finishing": data.finishing,
        "bahan.ukuran_x": data.ukuran_x,
        "bahan.ukuran_y": data.ukuran_y,
        "bahan.qty": data.qty,
        "biaya.total_bayar": data.total_bayar,
        "biaya.uang_muka": data.uang_muka,
        "biaya.sisa_bayar": data.sisa_bayar,
        "biaya.apakah_lunas": data.apakah_lunas,
    }

    return mongo.db.pesanan.find_one_and_update(find, {'$set': update}, return_document=True)


def delete_pesanan(no_transaksi: str):
    mongo.db.pesanan.remove({"_id": no_transaksi})


def lunasi(data: LunasPesananDto):
    find = {"_id": data.filter_id,
            "biaya.apakah_lunas": False}

    update = {
        "biaya.sisa_bayar": 0,
        "biaya.apakah_lunas": True,
        "diupdate": data.diupdate,
        "diupdate_oleh": data.diupdate_oleh,
        "petugas": data.diupdate_oleh,
        "id_petugas": data.id_petugas,
    }

    return mongo.db.pesanan.find_one_and_update(find, {'$set': update}, return_document=True)
