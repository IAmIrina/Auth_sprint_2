from http import HTTPStatus

from core.message_constants import (
    MSG_EMAIL_NOT_FOUND,
    MSG_USER_ALREADY_EXISTS,
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
from utils.model_func import get_user


class Profile(Resource):

    @swag_from(get_user_info)
    @jwt_required()
    def get(self):
        user_identity = get_jwt_identity()
        user = get_user(user_identity['id'])
        user_schema = UserSchema()
        return user_schema.dump(user), HTTPStatus.OK

    @swag_from(user_register)
    def post(self):
        data = request.json
        if not data.get('email'):
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, messages=MSG_EMAIL_NOT_FOUND)
        user = User.query.filter_by(email=data['email']).first()
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
        try:
            update_fields = ProfileChangeSchema().dump(data)
        except ValidationError as exc:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, message=exc.messages)
        user_id = get_jwt_identity().get('id')
        user_query = User.query.filter_by(id=user_id)
        user = get_user(user_id)

        personaldata_for_update = update_fields.pop('personal_data', None)
        if personaldata_for_update:
            UserPersonalData.query.filter_by(user_id=user_id).update(personaldata_for_update)
        if update_fields:
            user_query.update(update_fields)
        db.session.commit()
        return UserSchema().dump(user), HTTPStatus.OK
