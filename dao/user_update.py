from databases.db import mongo
from dto.user_dto import UserDto


def insert_user(data: UserDto):
    data_insert = {
        "user_id": data.user_id.upper(),
        "password": data.password,
        "name": data.name.upper(),
        "is_admin": data.is_admin,
        "is_staff": data.is_admin,
        "is_customer": data.is_customer,
        "phone": data.phone,
        "address": data.address,
        "join_date": data.join_date,
        "position": data.position
    }

    mongo.db.users.insert_one(data_insert)


def put_password(user_id: str, new_password: str):
    query = {"user_id": user_id}
    update = {'$set': {"password": new_password}}

    mongo.db.users.update_one(query, update)


def update_user(data: UserDto):
    find = {"user_id": data.user_id}
    update = {
        "name": data.name.upper(),
        "is_admin": data.is_admin,
        "is_staff": data.is_staff,
        "is_customer": data.is_customer,
        "phone": data.phone,
        "address": data.address,
        "join_date": data.join_date,
        "position": data.position
    }

    mongo.db.users.update_one(find, {'$set': update})


def delete_user(user_id: str):
    mongo.db.users.remove({"user_id": user_id.upper()})