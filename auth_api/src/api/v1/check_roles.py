
from http import HTTPStatus

from core.access import access_required
from core.message_constants import (
    MSG_ACCESS_TOKEN_NOT_FOUND,
    MSG_INVALID_TOKEN,
    MSG_USER_NOT_FOUND,
)
from flasgger import swag_from
from flask import request
from flask_jwt_extended import decode_token, jwt_required
from flask_restful import Resource, abort
from jwt.exceptions import DecodeError
from models.user import User
from schemas.roles import RoleSchema
from swager.profile import check_roles


class CheckRoles(Resource):

    @swag_from(check_roles)
    @jwt_required()
    @access_required()
    def post(self):
        data = request.json
        access_token = data.get("access_token")
        if not access_token:
            abort(HTTPStatus.NOT_FOUND, messages=MSG_ACCESS_TOKEN_NOT_FOUND)
        try:
            user_token_info = decode_token(access_token).get('sub')
        except DecodeError:
            abort(HTTPStatus.BAD_REQUEST, messages=MSG_INVALID_TOKEN)
        user = User.query.filter_by(id=user_token_info.get("id")).first()
        if not user:
            abort(HTTPStatus.NOT_FOUND, messages=MSG_USER_NOT_FOUND)
        return RoleSchema().dump(user.roles, many=True), HTTPStatus.OK
