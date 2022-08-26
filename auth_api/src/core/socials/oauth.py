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
    client_kwargs={'scope': 'email profile'},
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
    userinfo_endpoint='https://api.vk.com/method/users.get',
    client_kwargs={'scope': 'email'},
    compliance_fix=vk_compliance_fix,
    token_endpoint_auth_method='client_secret_post',
)
