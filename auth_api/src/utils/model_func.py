from http import HTTPStatus
from uuid import UUID

from core.message_constants import MSG_ROLE_NOT_FOUND, MSG_USER_NOT_FOUND
from flask_restful import abort
from models.user import Role, User, SocialAccount
from core.tracer import tracer


@tracer.start_as_current_span('get_user_from_db')
def get_user(user_id: UUID) -> User:
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(HTTPStatus.NOT_FOUND, messages=MSG_USER_NOT_FOUND)
    return user


@tracer.start_as_current_span('get_role_from_db')
def get_role(role_id: UUID) -> Role:
    role = Role.query.filter_by(id=role_id).first()
    if not role:
        abort(HTTPStatus.NOT_FOUND, messages=MSG_ROLE_NOT_FOUND)
    return role


@tracer.start_as_current_span('get_user_by_social_from_db')
def get_user_by_social(social_id: UUID, social_name: str) -> User:
    social = SocialAccount.query.filter_by(social_id=social_id, social_name=social_name).first()
    if social:
        user = User.query.filter_by(id=social.user_id).first()
        return user
    return None


@tracer.start_as_current_span('get_user_by_email_from_db')
def get_user_by_email(email: str) -> User:
    user = User.query.filter_by(email=email).first()
    return user
