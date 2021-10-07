from flask import Response, jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps

def roleCheck(role):
    def innerRoleCheck(function):
        @wraps(function)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if "role" in claims and claims["role"] == role:
                return function(*args, **kwargs)
            else:
                return jsonify(msg="Missing Authorization Header"), 401

        return decorator
    return innerRoleCheck