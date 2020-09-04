from databases.db import mongo


def get_one(email: str) -> dict:
    user = mongo.db.users.find_one({"email": email.upper()})
    return user


def get_one_without_password(email: str) -> dict:
    result = mongo.db.users.find_one(
        {"email": email.upper()}, {"password": 0})
    return result


def get_many_by_name(name: str) -> list:
    query_string = {'$regex': f'.*{name.upper()}.*'}

    user_collection = mongo.db.users.find(
        {"name": query_string}, {"password": 0})

    user_list = []

    for user in user_collection:
        user_list.append(user)

    return user_list


def get_many() -> list:
    user_list = []
    result = mongo.db.users.find({}, {"password": 0})
    for user in result:
        user_list.append(user)

    return user_list
