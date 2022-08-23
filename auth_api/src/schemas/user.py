from marshmallow_sqlalchemy import SQLAlchemySchema
from models.user import UserHistory


class UserHistorySchema(SQLAlchemySchema):
    class Meta:
        model = UserHistory
        load_instance = True
        fields = ('browser', 'date')
