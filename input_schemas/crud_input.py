from marshmallow import Schema, fields


class CrudSchemaCreate(Schema):
    nama = fields.Str(required=True)
    alamat = fields.Str(required=True)
    keterangan = fields.Str(required=True)