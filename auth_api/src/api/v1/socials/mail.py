"""Mail Social Login Routes."""
from http import HTTPStatus
import logging

from flask import Blueprint, request, url_for
from flask_restful import abort

from core.message_constants import MSG_SOCIAL_NETWORK_ERROR
from core.socials.oauth import oauth
from core.socials.social_auth import SocialAuth

SOCIAL_NAME = 'mail'

mail = Blueprint('mail', __name__, url_prefix=f'/{SOCIAL_NAME}')


@mail.route('/login')
def login():
    social = oauth.create_client(SOCIAL_NAME)
    redirect_uri = url_for('mail.authorize', _external=True)
    return social.authorize_redirect(redirect_uri)


@mail.route('/authorize')
def authorize():
    social = oauth.create_client(SOCIAL_NAME)
    token = social.authorize_access_token()
    resp = social.get('https://oauth.mail.ru/userinfo', params={'access_token': token['access_token']})
    try:
        user_info = resp.json()
    except BaseException:
        logging.exception('Error social login: %s', SOCIAL_NAME)
        abort(HTTPStatus.BAD_GATEWAY, message=MSG_SOCIAL_NETWORK_ERROR)
    try:
        user_data = dict(
            first_name=user_info.get('first_name'),
            last_name=user_info.get('last_name'),
            email=user_info.get('email'),
            social_id=user_info.get('id'),
            user_agent=str(request.user_agent),
        )
    except BaseException:
        logging.exception('Error social login: %s', SOCIAL_NAME)
        abort(HTTPStatus.BAD_GATEWAY, message=MSG_SOCIAL_NETWORK_ERROR)
    social = SocialAuth(SOCIAL_NAME)
    tokens = social.authorize(**user_data)
    return tokens, HTTPStatus.OK
