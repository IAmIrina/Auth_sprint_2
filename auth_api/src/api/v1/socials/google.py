"""GOOGLE Social Login Routes."""
from http import HTTPStatus
import logging

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
    try:
        token = social.authorize_access_token()
        oauth.google.userinfo()
        user_info = social.userinfo()
    except BaseException:
        logging.exception('Error social login: %s', SOCIAL_NAME)
        abort(HTTPStatus.BAD_GATEWAY, message=MSG_SOCIAL_NETWORK_ERROR)
    try:
        user_data = dict(
            first_name=user_info.get('given_name'),
            last_name=user_info.get('family_name'),
            email=user_info.get('email'),
            social_id=user_info.get('sub'),
            user_agent=str(request.user_agent),
        )
    except BaseException:
        logging.exception('Error social login: %s', SOCIAL_NAME)
        abort(HTTPStatus.BAD_GATEWAY, message=MSG_SOCIAL_NETWORK_ERROR)
    social = SocialAuth(SOCIAL_NAME)
    tokens = social.authorize(**user_data)
    return tokens, HTTPStatus.OK
