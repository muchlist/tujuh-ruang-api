from marshmallow import Schema, fields


class UserRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    name = fields.Str(required=True)
    is_admin = fields.Bool(required=True)
    is_staff = fields.Bool(required=True)
    is_customer = fields.Bool(required=True)
    phone = fields.Str(required=True)
    address = fields.Str(required=True)


class UserEditSchema(Schema):
    name = fields.Str(required=True)
    is_admin = fields.Bool(required=True)   
    is_staff = fields.Bool(required=True)
    is_customer = fields.Bool(required=True)
    phone = fields.Str(required=True)
    address = fields.Str(required=True)


class UserLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class UserChangePassSchema(Schema):
    password = fields.Str(required=True)
    new_password = fields.Str(required=True)