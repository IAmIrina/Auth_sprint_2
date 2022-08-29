from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_request(client):
    new_request = MagicMock()
    new_request.user_agent = "Firefox"
    mock_request = patch('api.v1.socials.google.request', new_request)
    yield mock_request
    mock_request.stop()


@pytest.fixture
def mock_authorize_access_token():
    mock_token = patch('authlib.integrations.flask_client.apps.FlaskOAuth2App.authorize_access_token')
    mock_token = mock_token.start()
    yield mock_token
    mock_token.stop()


@pytest.fixture
def mock_user_info(mock_request):
    mock_userinfo = patch('authlib.integrations.flask_client.apps.FlaskOAuth2App.userinfo')
    mock_userinfo = mock_userinfo.start()
    yield mock_userinfo
    mock_userinfo.stop()


@pytest.fixture
def mock_get_user_info(mock_request):
    mock_get = patch('authlib.integrations.flask_client.apps.FlaskOAuth2App.get')
    mock_get = mock_get.start()
    yield mock_get
    mock_get.stop()
