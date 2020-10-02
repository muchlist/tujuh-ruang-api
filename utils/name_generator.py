import random
import string
import time

def create_random_name():
    time_epoch = str(int(time.time()))
    random_string_name = random_string(5)
    return f'{time_epoch}-{random_string_name}.pdf'


def random_string(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))