from core.constants import LOGIN_REGEX, PASSWORD_REGEX
from marshmallow import Schema, fields, post_dump, post_load, validate
from models.user import User, UserPersonalData
from passlib.hash import pbkdf2_sha256
from schemas.roles import RoleSchema


class UserPersonalDataSchema(Schema):
    first_name = fields.String()
    second_name = fields.String()
    email = fields.Email()

    @post_load
    def create_personaldata(self, data, **kwargs):
        return UserPersonalData(**data)


class ProfileChangeSchema(Schema):
    login = fields.String()
    personal_data = fields.Nested(UserPersonalDataSchema)


class UserSchema(Schema):
    id = fields.UUID()
    login = fields.String()
    password = fields.String(validate=validate.Regexp(PASSWORD_REGEX))
    personal_data = fields.Nested(UserPersonalDataSchema)
    roles = fields.Nested(RoleSchema, many=True, required=False)

    class Meta:
        fields = ('id', 'login', 'password', 'personal_data', 'roles')
        ordered = True

    @post_dump
    def remove_password_field(self, data, **kwargs):
        data.pop('password', None)
        return data

    @post_load
    def create_profile(self, data, **kwargs):
        data['password'] = pbkdf2_sha256.hash(data['password'])
        return User(**data)


class UserRegisterSchema(Schema):
    login = fields.String(required=True, validate=validate.Regexp(LOGIN_REGEX))
    password = fields.String(required=True, validate=validate.Regexp(PASSWORD_REGEX))
    personal_data = fields.Nested(UserPersonalDataSchema)

    class Meta:
        fields = ('id', 'login', 'password', 'personal_data')
        ordered = True

    @post_load
    def create_profile(self, data, **kwargs):
        data['password'] = pbkdf2_sha256.hash(data['password'])
        return User(**data)
