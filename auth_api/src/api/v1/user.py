from http import HTTPStatus

from core.pagination import paginate_hook, pagination
from core.constants import DEVICES
from flasgger import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from models.user import UserHistory
from schemas.user import UserHistorySchema
from swager.profile import user_history


get_history_args = reqparse.RequestParser()
get_history_args.add_argument(
    'device',
    dest='device',
    location='args',
    required=True,
    choices=DEVICES,
    help=f"Required device type: {','.join(DEVICES)}",
)


class UserActivity(Resource):

    @swag_from(user_history)
    @jwt_required()
    def get(self):
        args = get_history_args.parse_args()
        user_id = get_jwt_identity().get('id')
        user_history = UserHistory.query.filter_by(user_id=user_id, user_device_type=args.device)
        return pagination.paginate(
            user_history,
            UserHistorySchema(),
            True,
            pagination_schema_hook=paginate_hook,
        ), HTTPStatus.OK
