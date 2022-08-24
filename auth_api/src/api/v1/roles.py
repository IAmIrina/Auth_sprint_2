
from http import HTTPStatus

from core.access import access_required
from core.message_constants import (
    MSG_INVALID_URL,
    MSG_ROLE_ALREADY_EXISTS,
    MSG_USER_ROLE_ALREADY_DELETE,
    MSG_USER_ROLE_ALREADY_EXIST,
)
from core.pagination import paginate_hook, pagination
from db.storage import db
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort
from marshmallow.exceptions import ValidationError
from models.user import Role
from schemas.roles import RoleSchema
from utils.model_func import get_role, get_user


class Roles(Resource):

    @jwt_required()
    @access_required()
    def get(self, role_id=None):
        role_schema = RoleSchema()
        if role_id:
            role = get_role(role_id)
            return role_schema.dump(role), HTTPStatus.OK
        return pagination.paginate(
            Role,
            role_schema,
            True,
            pagination_schema_hook=paginate_hook,
        ), HTTPStatus.OK

    @jwt_required()
    @access_required()
    def post(self, role_id=None):
        if role_id:
            abort(HTTPStatus.BAD_REQUEST, messages=MSG_INVALID_URL)
        data = request.json
        role_schema = RoleSchema()
        try:
            new_role = role_schema.load(data)
        except ValidationError as exc:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, message=exc.messages)

        role = Role.query.filter_by(name=new_role['name']).first()
        if role:
            abort(HTTPStatus.CONFLICT, message=MSG_ROLE_ALREADY_EXISTS.format(name=role.name))

        role = Role(**data)
        db.session.add(role)
        db.session.commit()
        return role_schema.dump(role), HTTPStatus.CREATED

    @jwt_required()
    @access_required()
    def delete(self, role_id):
        role = get_role(role_id)
        db.session.delete(role)
        db.session.commit()
        return {}, HTTPStatus.NO_CONTENT


class RolesUser(Resource):

    @jwt_required()
    @access_required()
    def get(self, user_id, role_id=None):
        if role_id:
            abort(HTTPStatus.BAD_REQUEST, messages=MSG_INVALID_URL)
        user = get_user(user_id)
        return RoleSchema().dump(user.roles, many=True), HTTPStatus.OK

    @jwt_required()
    @access_required()
    def post(self, user_id, role_id):
        user = get_user(user_id)
        role = get_role(role_id)
        if role in user.roles:
            abort(
                HTTPStatus.CONFLICT,
                messages=MSG_USER_ROLE_ALREADY_EXIST.format(user_name=user.email, role_name=role.name),
            )
        user.roles.append(role)
        db.session.commit()
        return RoleSchema().dump(user.roles, many=True), HTTPStatus.OK

    @jwt_required()
    @access_required()
    def delete(self, user_id, role_id):
        user = get_user(user_id)
        role = get_role(role_id)
        if role in user.roles:
            user.roles.remove(role)
        else:
            abort(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                messages=MSG_USER_ROLE_ALREADY_DELETE.format(user_name=user.email, role_name=role.name),
            )
        db.session.commit()
        return {}, HTTPStatus.NO_CONTENT
