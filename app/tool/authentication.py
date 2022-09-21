from ..env.config import hash_func


def get_hash_password(password: str):
    hash_password = hash_func.hash(password)
    return hash_password

# def verify_password(pass)