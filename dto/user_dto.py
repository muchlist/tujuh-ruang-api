import collections

UserDto = collections.namedtuple(
    'User', ['email', 'password', 'name',  'is_admin', 'is_staff', 'is_customer', 'phone', 'address'])
