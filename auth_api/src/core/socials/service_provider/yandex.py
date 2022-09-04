import logging
from http import HTTPStatus

from flask_restful import abort

from core.message_constants import MSG_SOCIAL_NETWORK_ERROR
from core.settings import settings
from core.socials.service_provider.oauth_service import OauthServiceProvider
from core.socials.social_auth import SocialUser


class Yandex(OauthServiceProvider):
    """Yandex Oauth 2.0 settings."""
    name = 'yandex'

    @staticmethod
    def parse_user_info(user_info: dict, token: dict) -> SocialUser:
        try:
            user_data = SocialUser(
                first_name=user_info.get('first_name'),
                last_name=user_info.get('last_name'),
                email=user_info.get('emails')[0],
                social_id=user_info.get('id'),
            )
        except BaseException:
            logging.exception('Error social login: %s', Yandex.name)
            abort(HTTPStatus.BAD_GATEWAY, message=MSG_SOCIAL_NETWORK_ERROR)
        return user_data

    def get_params(self):
        return dict(name=self.name, **settings.yandex.dict())
