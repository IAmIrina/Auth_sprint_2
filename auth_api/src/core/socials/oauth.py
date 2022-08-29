import json

from authlib.integrations.flask_client import OAuth

oauth = OAuth()

google = oauth.register(
    name='google',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
)


def vk_compliance_fix(session):
    """Transform VK access token response to standart format."""
    def _fix(resp):
        resp.raise_for_status()
        token = resp.json()
        token['token_type'] = 'Bearer'
        resp._content = json.dumps(token).encode('utf-8')
        return resp
    session.register_compliance_hook('access_token_response', _fix)


vk = oauth.register(
    name='vk',
    access_token_url='https://oauth.vk.com/access_token',
    access_token_params=None,
    authorize_url='https://oauth.vk.com/authorize',
    authorize_params=None,
    api_base_url='https://api.vk.com/method/',
    client_kwargs={'scope': 'email'},
    compliance_fix=vk_compliance_fix,
    token_endpoint_auth_method='client_secret_post',
)

yandex = oauth.register(
    name='yandex',
    access_token_params=None,
    access_token_url='https://oauth.yandex.ru/token',
    authorize_params=None,
    userinfo_endpoint='https://login.yandex.ru/info',
    authorize_url='https://oauth.yandex.ru/authorize',
    client_kwargs={
        'scope': 'login:info login:email'
    }
)

mail = oauth.register(
    name='mail',
    access_token_params=None,
    access_token_url='https://oauth.mail.ru/token',
    authorize_params=None,
    authorize_url='https://oauth.mail.ru/login',
    client_kwargs={
        'scope': 'userinfo'
    },
)
