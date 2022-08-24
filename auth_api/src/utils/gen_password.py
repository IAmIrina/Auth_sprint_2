import string
from secrets import choice as secrets_choice

PASSWORD_LENGTH = 16


def generate_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets_choice(alphabet) for _ in range(PASSWORD_LENGTH))
