"""Social Login Route."""
from http import HTTPStatus

from flask import Blueprint, request, url_for
from flask_restful import abort

from core.message_constants import MSG_SOCIAL_NOT_SUPPORTED
from core.socials.oauth import SOCIALS, oauth
from core.socials.social_auth import SocialAuth

route = 'socials'

socials = Blueprint(route, __name__, url_prefix=f'/{route}')


@socials.route('/login/<name>')
def login(name):
    client = oauth.create_client(name)
    if not client:
        abort(HTTPStatus.NOT_FOUND, message=MSG_SOCIAL_NOT_SUPPORTED.format(name=name))
    redirect_uri = url_for('socials.auth', name=name, _external=True)
    return client.authorize_redirect(redirect_uri)


@socials.route('/auth/<name>')
def auth(name):
    client = oauth.create_client(name)
    if not client:
        abort(HTTPStatus.NOT_FOUND, message=MSG_SOCIAL_NOT_SUPPORTED.format(name=name))
    token = client.authorize_access_token()
    user_info = client.userinfo(params={'access_token': token.get('access_token')})
    for social in SOCIALS:
        if social.name == name:
            user_info = social.parse_user_info(user_info=user_info, token=token)
    user_info.user_agent = str(request.user_agent)
    social_auth = SocialAuth(name)
    tokens = social_auth.authorize(user_info)
    return tokens, HTTPStatus.OK
