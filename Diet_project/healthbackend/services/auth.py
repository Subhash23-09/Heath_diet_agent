from flask import request
from functools import wraps
from healthbackend.config.settings import API_KEY
from healthbackend.utils.exceptions import AuthError

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.headers.get("x-api-key") != API_KEY:
            raise AuthError("Invalid API key")
        return func(*args, **kwargs)
    return wrapper
