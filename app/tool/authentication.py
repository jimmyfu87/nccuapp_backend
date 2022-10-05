from http import cookies

from requests import session
from ..env.config import hash_func
from fastapi import Request
from ..env.config import redis


def get_hash_password(password: str):
    hash_password = hash_func.hash(password)
    return hash_password


def verify_cookies(request: Request):
    if request.cookies:
        if 'sid' in list(request.cookies.keys()):
            session_id = request.cookies['sid']
            member_id = redis.get(session_id)
            if member_id:
                return {'success': True, 'member_id': member_id}
            else:
                return {'success': False, 'message': 'Cookie outdate, please login again!!'}
        else:
            return {'success': False, 'message': 'No cookie!!'}
    else:
        return {'success': False, 'message': 'No cookie!!'}
