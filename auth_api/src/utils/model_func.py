from http import HTTPStatus
from uuid import UUID

from core.message_constants import MSG_ROLE_NOT_FOUND, MSG_USER_NOT_FOUND
from flask_restful import abort
from models.user import Role, User


def get_user(user_id: UUID) -> User:
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(HTTPStatus.NOT_FOUND, messages=MSG_USER_NOT_FOUND)
    return user


def get_role(role_id: UUID) -> Role:
    role = Role.query.filter_by(id=role_id).first()
    if not role:
        abort(HTTPStatus.NOT_FOUND, messages=MSG_ROLE_NOT_FOUND)
    return role
