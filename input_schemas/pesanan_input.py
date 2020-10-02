from marshmallow import Schema, fields


class BuatPesananSchema(Schema):
    nama_pesanan = fields.Str(required=True)
    nama_file = fields.Str(required=True)
    ukuran_x = fields.Int(required=True)
    # Diandroidnya yang diatur apakah satu ukuran atau tidak
    ukuran_y = fields.Int(required=True)
    qty = fields.Int(required=True)
    uang_muka = fields.Int(required=True)
    apakah_lunas = fields.Bool(required=True)
    finishing = fields.Str(required=True)
    id_bahan = fields.Str(required=True)
    id_pelanggan = fields.Str(required=True)


class EditPesananSchema(Schema):
    timestamp_filter = fields.DateTime(required=True)

    nama_pesanan = fields.Str(required=True)
    nama_file = fields.Str(required=True)
    ukuran_x = fields.Int(required=True)
    ukuran_y = fields.Int(required=True)
    qty = fields.Int(required=True)
    uang_muka = fields.Int(required=True)
    apakah_lunas = fields.Bool(required=True)
    finishing = fields.Str(required=True)
    id_bahan = fields.Str(required=True)
    id_pelanggan = fields.Str(required=True)


class ReportsPesananSchema(Schema):
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
