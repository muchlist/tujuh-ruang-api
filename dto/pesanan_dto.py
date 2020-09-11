from datetime import datetime
from typing import NamedTuple, List


class PesananDto(NamedTuple):
    no_transaksi: str
    nama_pesanan: str
    nama_file: str
    ukuran_x: str
    ukuran_y: str    # Diandroidnya yang diatur apakah satu ukuran atau tidak
    qty: int
    total_bayar: int
    uang_muka: int
    sisa_bayar: int
    apakah_lunas: bool
    petugas: str
    id_petugas: str
    finishing: str
    bahan: str
    id_bahan: str
    harga_bahan: int
    pelanggan: str
    id_pelanggan: str
    dibuat: datetime
    dibuat_oleh: str
    diupdate: datetime
    diupdate_oleh: str

class EditPesananDto(NamedTuple):
    filter_id: str
    filter_timestamp: datetime

    nama_pesanan: str
    nama_file: str
    ukuran_x: str
    ukuran_y: str    # Diandroidnya yang diatur apakah satu ukuran atau tidak
    qty: int
    total_bayar: int
    uang_muka: int
    sisa_bayar: int
    apakah_lunas: bool
    petugas: str
    id_petugas: str
    finishing: str
    bahan: str
    id_bahan: str
    harga_bahan: int
    pelanggan: str
    id_pelanggan: str
    dibuat: datetime
    dibuat_oleh: str
    diupdate: datetime
    diupdate_oleh: str

class LunasPesananDto(NamedTuple):
    filter_id: str
    filter_timestamp: datetime
    diupdate: datetime
    diupdate_oleh: str
