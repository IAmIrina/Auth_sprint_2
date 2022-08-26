"""GOOGLE Social Login Routes."""
from http import HTTPStatus

from flask import Blueprint, request, url_for
from flask_restful import abort

from core.message_constants import MSG_SOCIAL_NETWORK_ERROR
from core.socials.oauth import oauth
from core.socials.social_auth import SocialAuth

SOCIAL_NAME = 'google'

google = Blueprint('google', __name__, url_prefix=f'/{SOCIAL_NAME}')


@google.route('/login')
def login():
    social = oauth.create_client(SOCIAL_NAME)
    redirect_uri = url_for('google.authorize', _external=True)
    return social.authorize_redirect(redirect_uri)


@google.route('/authorize')
def authorize():

    social = oauth.create_client(SOCIAL_NAME)
    token = social.authorize_access_token()
    resp = social.get('userinfo')
    print(resp)
    try:
        user_info = resp.json()
    except BaseException:
        abort(HTTPStatus.BAD_GATEWAY, message=MSG_SOCIAL_NETWORK_ERROR)
    print(user_info)
    try:
        user_data = dict(
            first_name=user_info.get('given_name'),
            last_name=user_info.get('family_name'),
            email=user_info.get('email'),
            social_id=user_info.get('id'),
            user_agent=str(request.user_agent),
        )
    except BaseException:
        abort(HTTPStatus.BAD_GATEWAY, message=MSG_SOCIAL_NETWORK_ERROR)
    print(user_data)
    social = SocialAuth(SOCIAL_NAME)
    tokens = social.authorize(**user_data)
    return tokens, HTTPStatus.OK
