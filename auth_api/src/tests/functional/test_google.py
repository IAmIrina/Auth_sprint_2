"""Test Google Auth."""
from http import HTTPStatus
from unittest.mock import MagicMock


def test_google_auth_new_user(mock_user_info, mock_authorize_access_token, client):
    """Google OAuth for new user."""
    test_user_data = dict(
        given_name='Brad',
        family_name='Pitt',
        email='bp@gmail.com',
        sub='id_12345678',
    )
    mock_authorize_access_token.return_value.status_code = HTTPStatus.OK
    mock_user_info.return_value = test_user_data

    response = client.get('/socials/login/google')
    assert response.status_code == HTTPStatus.FOUND

    response = client.get('/socials/auth/google')
    tokens = response.json

    assert response.status_code == HTTPStatus.OK
    assert bool(tokens.get('access_token'))
    assert bool(tokens.get('refresh_token'))


def test_google_auth_user_already_exists(mock_user_info, mock_authorize_access_token, client, test_user):
    """Google OAuth for registered user."""
    test_user_data = dict(
        given_name=test_user['personal_data']['first_name'],
        family_name=test_user['personal_data']['second_name'],
        email=test_user['email'],
        sub='id_12345678',
    )
    mock_authorize_access_token.return_value.status_code = HTTPStatus.OK
    mock_user_info.return_value = test_user_data

    response = client.get('/socials/login/google')
    assert response.status_code == HTTPStatus.FOUND

    response = client.get('/socials/auth/google')
    tokens = response.json

    assert response.status_code == HTTPStatus.OK
    assert bool(tokens.get('access_token'))
    assert bool(tokens.get('refresh_token'))
