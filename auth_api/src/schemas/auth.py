from datetime import datetime

from core.constants import PASSWORD_REGEX
from marshmallow import Schema, fields, post_dump, validate


class ChangePassword(Schema):
    old = fields.String(required=True)
    new = fields.String(required=True, validate=validate.Regexp(PASSWORD_REGEX))


class JWTSchema(Schema):
    id = fields.String(required=True)
    created_at: str = fields.String()

    @post_dump(pass_many=True)
    def created_time(self, data, **kwargs):
        data['created_at'] = datetime.utcnow().isoformat()
        return data
