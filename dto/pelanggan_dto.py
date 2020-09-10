from datetime import datetime
from typing import NamedTuple, List


class PelangganDto(NamedTuple):
    id_pelanggan: str
    nama: str
    email: str
    hp: str
    alamat: str
    total_transaksi_lunas: int
    total_hutang: int
    dibuat: datetime
    dibuat_oleh: str
    diupdate: datetime
    diupdate_oleh: str
    aktif: bool

class EditPelangganDto(NamedTuple):
    filter_id: str
    filter_timestamp: datetime

    id_pelanggan: str
    nama: str
    email: str
    hp: str
    alamat: str