from marshmallow import Schema, fields


class RoleSchema(Schema):

    id = fields.String()
    name = fields.String(required=True)
