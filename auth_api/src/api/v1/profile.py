from http import HTTPStatus

from core.message_constants import (
    MSG_EMPTY_LOGIN,
    MSG_LOGIN_NOT_FOUND,
    MSG_USER_ALREADY_EXISTS,
    MSG_USER_NOT_FOUND,
)
from db.storage import db
from flasgger import swag_from
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, abort
from marshmallow.exceptions import ValidationError
from models.user import User, UserPersonalData
from schemas.profile import ProfileChangeSchema, UserRegisterSchema, UserSchema
from swager.profile import get_user_info, user_change_schema, user_register


class Profile(Resource):

    @swag_from(get_user_info)
    @jwt_required()
    def get(self):
        user_identity = get_jwt_identity()
        user = User.query.get(user_identity['id'])
        if not user:
            abort(HTTPStatus.NOT_FOUND, message=MSG_USER_NOT_FOUND)
        user_schema = UserSchema()
        return user_schema.dump(user), HTTPStatus.OK

    @swag_from(user_register)
    def post(self):
        data = request.json
        if not data.get('login'):
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, messages=MSG_LOGIN_NOT_FOUND)
        user = User.query.filter_by(login=data['login']).first()
        if user:
            abort(HTTPStatus.CONFLICT, message=MSG_USER_ALREADY_EXISTS)
        user_register_schema = UserRegisterSchema()
        profile_schema = UserSchema()
        try:
            profile = user_register_schema.load(data)
        except ValidationError as exc:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, message=exc.messages)
        db.session.add(profile)
        db.session.commit()
        return profile_schema.dump(profile), HTTPStatus.CREATED

    @swag_from(user_change_schema)
    @jwt_required()
    def patch(self):
        data = request.json
        if 'login' in data.keys() and not data.get('login'):
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, message=MSG_EMPTY_LOGIN)
        try:
            update_fields = ProfileChangeSchema().dump(data)
        except ValidationError as exc:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, message=exc.messages)
        user_id = get_jwt_identity().get('id')
        user_query = User.query.filter_by(id=user_id)
        user = user_query.first()
        if not user:
            abort(HTTPStatus.NOT_FOUND, message=MSG_USER_NOT_FOUND)
        login = update_fields.get('login')
        if login:
            exist_user_with_login = User.query.filter_by(login=login).first()
            if exist_user_with_login and str(exist_user_with_login.id) != user_id:
                abort(HTTPStatus.CONFLICT, message=MSG_USER_ALREADY_EXISTS)
        personaldata_for_update = update_fields.pop('personal_data', None)
        if personaldata_for_update:
            UserPersonalData.query.filter_by(user_id=user_id).update(personaldata_for_update)
        if update_fields:
            user_query.update(update_fields)
        db.session.commit()
        return UserSchema().dump(user), HTTPStatus.OK
