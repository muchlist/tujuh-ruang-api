from databases.db import mongo
from dto.user_dto import UserDto


def insert_user(data: UserDto):
    data_insert = {
        "email": data.email.upper(),
        "password": data.password,
        "name": data.name.upper(),
        "is_admin": data.is_admin,
        "is_staff": data.is_admin,
        "is_customer": data.is_customer,
        "phone": data.phone,
        "address": data.address,
    }

    mongo.db.users.insert_one(data_insert)


def put_password(email: str, new_password: str):
    query = {"email": email}
    update = {'$set': {"password": new_password}}

    mongo.db.users.update_one(query, update)


def update_user(data: UserDto):
    find = {"email": data.email}
    update = {
        "name": data.name.upper(),
        "is_admin": data.is_admin,
        "is_staff": data.is_staff,
        "is_customer": data.is_customer,
        "phone": data.phone,
        "address": data.address,
    }

    mongo.db.users.update_one(find, {'$set': update})


def delete_user(email: str):
    mongo.db.users.remove({"email": email.upper()})