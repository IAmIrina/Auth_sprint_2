"""Access decorators."""
from functools import wraps
from http import HTTPStatus
from typing import Tuple

from core.message_constants import MSG_FORBIDDEN
from db.cache_engine import jwt_refresh_cache
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flask_restful import abort
from models.user import User
from schemas.auth import JWTSchema


def create_token_pair(user: User, fresh=False) -> Tuple[dict, str]:
    jwt_schema = JWTSchema()
    identity = jwt_schema.dump(user)
    tokens = dict(
        access_token=create_access_token(identity, fresh=fresh),
        refresh_token=create_refresh_token(identity),
    )
    cache_key = jwt_refresh_cache.gen_cache_key(**identity)
    jwt_refresh_cache.set(cache_key, ' ')
    return identity, tokens


def access_required(roles: list = ["Admin"]):
    """Check user access role decorator."""
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            user_id = get_jwt_identity().get('id')
            user = User.query.filter_by(id=user_id).first()

            if not user:
                abort(HTTPStatus.FORBIDDEN, message=MSG_FORBIDDEN)

            if not any(user_role.name in roles for user_role in user.roles):
                abort(HTTPStatus.FORBIDDEN, message=MSG_FORBIDDEN)

            return fn(*args, **kwargs)

        return decorated_view
    return wrapper
