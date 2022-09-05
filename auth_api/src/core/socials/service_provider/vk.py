import json
import logging
from http import HTTPStatus

from flask_restful import abort

from core.message_constants import MSG_SOCIAL_NETWORK_ERROR
from core.settings import settings
from core.socials.service_provider.oauth_service import OauthServiceProvider
from core.socials.social_auth import SocialUser


class VKontakte(OauthServiceProvider):
    name = 'vk'

    @staticmethod
    def parse_user_info(user_info: dict, token: dict) -> SocialUser:
        try:
            response = user_info.get('response')
            user_info = response[0]
        except BaseException:
            logging.exception('Error social login %s.', VKontakte.name)
            abort(HTTPStatus.BAD_GATEWAY, message=MSG_SOCIAL_NETWORK_ERROR)
        try:
            user_data = SocialUser(
                first_name=user_info.get('first_name'),
                last_name=user_info.get('last_name'),
                email=token.get('email'),
                social_id=str(token.get('user_id')),
            )
        except BaseException:
            logging.exception('Error social login %s.', VKontakte.name)
            abort(HTTPStatus.BAD_GATEWAY, message=MSG_SOCIAL_NETWORK_ERROR)
        return user_data

    @staticmethod
    def compliance_fix(session):
        """Transform VK access token response to standart format."""
        def _fix(resp):
            resp.raise_for_status()
            token = resp.json()
            token['token_type'] = 'Bearer'
            resp._content = json.dumps(token).encode('utf-8')
            return resp
        session.register_compliance_hook('access_token_response', _fix)

    def get_userinfo_params(**kwargs) -> dict:
        """Dinamic request params for userinfo endpoint."""
        return {}

    def get_params(self):
        return dict(name=self.name, **settings.vk.dict(), compliance_fix=VKontakte.compliance_fix)
