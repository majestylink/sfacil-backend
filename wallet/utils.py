import secrets
import string


def generate_reference():
    alphabet = string.ascii_letters + string.digits
    while True:
        ref = ''.join(secrets.choice(alphabet) for i in range(10))
        if any(c.islower() for c in ref) and any(c.isupper() for c in ref) and any(c.isdigit() for c in ref):
            break
    return ref
