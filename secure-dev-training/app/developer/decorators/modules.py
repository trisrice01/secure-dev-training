from flask import jsonify
from app import db
from app.models.modules import Module


MODULE_THEORY = "MODULE_THEORY"
MODULE_CTF = "MODULE_CTF"
MODULE_CODE = "MODULE_CODE"

def module_enabled(module_constant):
    def decorator(func):
        def wrapper(*args, **kwargs):
            module = Module.query.filter_by(constant=module_constant).first()
            if not module.is_enabled:
                return jsonify({
                    "error": True,
                    "message": "Service unavailable"
                }), 503
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper

    return decorator
            