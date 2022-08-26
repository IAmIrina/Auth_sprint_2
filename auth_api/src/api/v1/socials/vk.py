"""VK Social Login Routes."""
from http import HTTPStatus

from flask import Blueprint, request, url_for
from flask_restful import abort

from core.message_constants import MSG_SOCIAL_NETWORK_ERROR
from core.socials.oauth import oauth
from core.socials.social_auth import SocialAuth

SOCIAL_NAME = 'vk'

vkontakte = Blueprint('vkontakte', __name__, url_prefix=f'/{SOCIAL_NAME}')


@vkontakte.route('/login')
def login():
    social = oauth.create_client(SOCIAL_NAME)
    redirect_uri = url_for('vkontakte.authorize', _external=True)
    return social.authorize_redirect(redirect_uri)


@vkontakte.route('/authorize')
def authorize():
    social = oauth.create_client(SOCIAL_NAME)

    token = social.authorize_access_token()
    resp = social.get('users.get', params={'v': '5.131'})
    try:
        response = resp.json()
        response = response.get('response')
        user_info = response[0]
    except BaseException:
        abort(HTTPStatus.BAD_GATEWAY, message=MSG_SOCIAL_NETWORK_ERROR)

    try:
        user_data = dict(
            first_name=user_info.get('first_name'),
            last_name=user_info.get('last_name'),
            email=token.get('email'),
            social_id=str(token.get('user_id')),
            user_agent=str(request.user_agent),
        )
    except BaseException:
        abort(HTTPStatus.BAD_GATEWAY, message=MSG_SOCIAL_NETWORK_ERROR)

    social = SocialAuth(SOCIAL_NAME)
    tokens = social.authorize(**user_data)
    return tokens, HTTPStatus.OK
