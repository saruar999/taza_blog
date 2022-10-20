import random
import string


def generate_verification_code(length=6):
    return ''.join(random.choice(string.digits) for _ in range(length))


def generate_random_string(length=5):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))