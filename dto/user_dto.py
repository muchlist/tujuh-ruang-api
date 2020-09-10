import collections

UserDto = collections.namedtuple(
    'User', ['user_id', 'password', 'name',  'is_admin', 'is_staff', 'is_customer', 'phone', 'address', "join_date", "position"])
