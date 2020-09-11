from marshmallow import Schema, fields


class BahanRegisterSchema(Schema):
    nama = fields.Str(required=True)
    harga = fields.Int(required=True)
    satuan = fields.Str(required=True)
    punya_dimensi = fields.Bool(required=True)
    spek = fields.Str(required=True)


class BahanEditSchema(Schema):
    timestamp_filter = fields.DateTime(required=True)

    nama = fields.Str(required=True)
    harga = fields.Int(required=True)
    satuan = fields.Str(required=True)
    punya_dimensi = fields.Bool(required=True)
    spek = fields.Str(required=True)
