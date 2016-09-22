import random
import string

PORT_START = 40000
PORT_END = 50000


def random_string(l=12):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(l))


data = [{'id': n,
         'name': random_string(),
         'port': n,
         'tag': 'test-tag1'} for n in range(PORT_START, PORT_END)]
