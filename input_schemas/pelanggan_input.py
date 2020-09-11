from marshmallow import Schema, fields

class PelangganRegisterSchema(Schema):
    id_pelanggan = fields.Str(required=True)
    nama = fields.Str(required=True)
    email = fields.Email(required=True)
    hp = fields.Str(required=True)
    alamat = fields.Str(required=True)


class PelangganEditSchema(Schema):
    timestamp_filter = fields.DateTime(required=True)

    nama = fields.Str(required=True)
    email = fields.Email(required=True)
    hp = fields.Str(required=True)
    alamat = fields.Str(required=True)

