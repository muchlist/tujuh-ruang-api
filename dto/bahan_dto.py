from datetime import datetime
from typing import NamedTuple, List


class BahanDto(NamedTuple):
    nama: str
    harga: int
    satuan: str
    punya_dimensi: bool
    diupdate: datetime
    diupdate_oleh: str
    spek: str
    image: str


class EditBahanDto(NamedTuple):
    filter_id: str
    filter_timestamp: datetime
    nama: str
    harga: int
    satuan: str
    punya_dimensi: bool
    diupdate: datetime
    diupdate_oleh: str
    spek: str
