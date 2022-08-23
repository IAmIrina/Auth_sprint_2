
from http import HTTPStatus
from typing import Tuple

from core.message_constants import (
    MSG_INVALID_CREDENTIALS,
    MSG_PASSWORD_CHANGED,
    MSG_USER_NOT_FOUND,
)
from db.storage import db
from flasgger import swag_from
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, abort
from marshmallow.exceptions import ValidationError
from models.user import User
from passlib.hash import pbkdf2_sha256
from schemas.auth import ChangePassword
from swager.auth import change_password


class Password(Resource):

    @swag_from(change_password)
    @jwt_required(fresh=True)
    def post(self) -> Tuple[dict, int]:
        """Change password view."""

        passwords = ChangePassword()
        try:
            passwords = passwords.load(request.json)
        except ValidationError as exc:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, message=exc.messages)

        user_identity = get_jwt_identity()
        user = User.query.get(user_identity.get('id'))
        if not user:
            abort(HTTPStatus.NOT_FOUND, message=MSG_USER_NOT_FOUND)

        if not pbkdf2_sha256.verify(passwords['old'], user.password):
            abort(HTTPStatus.UNAUTHORIZED, message=MSG_INVALID_CREDENTIALS)

        user.password = pbkdf2_sha256.hash(passwords['new'])
        db.session.commit()
        return {'msg': MSG_PASSWORD_CHANGED}, HTTPStatus.OK
