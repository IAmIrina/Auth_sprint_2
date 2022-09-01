import logging
from http import HTTPStatus

from core.access import create_token_pair
from core.message_constants import (
    MSG_INTERNAL_SERVER_ERROR,
    MSG_INVALID_CREDENTIALS,
    MSG_TOKEN_REVOKED,
)
from db.cache_engine import (
    jwt_blocklist,
    jwt_refresh_blocklist,
    jwt_refresh_cache,
)
from db.storage import db
from flasgger import swag_from
from flask import request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource, abort
from models.user import User, UserHistory
from swager.auth import login, logout, refresh
from utils.model_func import get_user
from utils.parse_user_agent import get_device_type


class Login(Resource):

    @swag_from(login)
    def post(self):
        """Login Method.

        Basic authorization required.
        """
        auth = request.authorization

        if not auth:
            abort(HTTPStatus.UNAUTHORIZED, message=MSG_INVALID_CREDENTIALS)

        user = User.query.filter_by(email=auth.username).first()

        if user:
            if user.verify_password(auth.password):
                _, tokens = create_token_pair(user, fresh=True)
                user_agent = str(request.user_agent)
                user.history.append(
                    UserHistory(
                        browser=user_agent,
                        user_device_type=get_device_type(user_agent),
                    ))
                db.session.commit()
                return tokens, HTTPStatus.OK

        abort(HTTPStatus.UNAUTHORIZED, message=MSG_INVALID_CREDENTIALS)


class Logout(Resource):

    @swag_from(logout)
    @jwt_required(verify_type=False)
    def delete(self):
        """Logout method."""
        token = get_jwt()
        jti = token['jti']
        ttype = token['type']

        cache_key = jwt_blocklist.gen_cache_key(jti=jti)
        try:
            if ttype == 'access':
                jwt_blocklist.set(cache_key, ' ')
            else:
                jwt_refresh_blocklist.set(cache_key, ' ')
        except Exception:
            logging.exception(MSG_INTERNAL_SERVER_ERROR)
            return {'msg': MSG_INTERNAL_SERVER_ERROR}, HTTPStatus.INTERNAL_SERVER_ERROR

        return {'msg': MSG_TOKEN_REVOKED.format(type=ttype.capitalize())}, HTTPStatus.NO_CONTENT


class Refresh(Resource):

    @swag_from(refresh)
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()

        cache_key = jwt_refresh_cache.gen_cache_key(**identity)
        jwt_refresh_cache.delete(cache_key)

        user = get_user(identity['id'])

        identity, tokens = create_token_pair(user)
        return tokens, HTTPStatus.OK
