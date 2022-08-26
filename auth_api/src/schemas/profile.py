from marshmallow import Schema, fields, post_dump, post_load, validate

from core.constants import FAKE_MAIL_DOMAIN, PASSWORD_REGEX
from models.user import User, UserPersonalData
from schemas.roles import RoleSchema


class UserPersonalDataSchema(Schema):
    first_name = fields.String()
    second_name = fields.String()

    @post_load
    def create_personaldata(self, data, **kwargs):
        return UserPersonalData(**data)


class ProfileChangeSchema(Schema):
    personal_data = fields.Nested(UserPersonalDataSchema)


class UserSchema(Schema):
    id = fields.UUID()
    email = fields.Email()
    password = fields.String(validate=validate.Regexp(PASSWORD_REGEX))
    personal_data = fields.Nested(UserPersonalDataSchema)
    roles = fields.Nested(RoleSchema, many=True, required=False)

    class Meta:
        fields = ('id', 'email', 'password', 'personal_data', 'roles')
        ordered = True

    @post_dump
    def remove_password_field(self, data, **kwargs):
        data.pop('password', None)
        if data['email'].endswith(FAKE_MAIL_DOMAIN):
            data['email'] = None
        return data

    @post_load
    def create_profile(self, data, **kwargs):
        return User(**data)


class UserRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Regexp(PASSWORD_REGEX))
    personal_data = fields.Nested(UserPersonalDataSchema)

    class Meta:
        fields = ('id', 'email', 'password', 'personal_data')
        ordered = True

    @post_load
    def create_profile(self, data, **kwargs):
        return User(**data)
