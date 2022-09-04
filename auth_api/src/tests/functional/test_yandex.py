from http import HTTPStatus
from unittest.mock import MagicMock


def test_yandex_auth_new_user(mock_user_info, mock_authorize_access_token, client):
    test_user_data = dict(
        first_name='Alex',
        last_name='Ivanov',
        emails=['alex@mail.ru'],
        id='57868543',
    )
    mock_authorize_access_token.return_value.status_code = HTTPStatus.OK
    mock_user_info.return_value = test_user_data

    response = client.get('/socials/login/yandex')
    assert response.status_code == HTTPStatus.FOUND

    response = client.get('/socials/auth/yandex')
    tokens = response.json

    assert response.status_code == HTTPStatus.OK
    assert bool(tokens.get('access_token'))
    assert bool(tokens.get('refresh_token'))


def test_google_auth_user_already_exists(mock_user_info, mock_authorize_access_token, client, test_user):
    """VK OAuth for registered user."""
    test_user_data = dict(
        first_name=test_user['personal_data']['first_name'],
        last_name=test_user['personal_data']['second_name'],
        emails=[test_user['email']],
        id='57868543',
    )
    mock_authorize_access_token.return_value.status_code = HTTPStatus.OK
    mock_user_info.return_value = test_user_data

    response = client.get('/socials/login/yandex')
    assert response.status_code == HTTPStatus.FOUND

    response = client.get('/socials/auth/yandex')
    tokens = response.json

    assert response.status_code == HTTPStatus.OK
    assert bool(tokens.get('access_token'))
    assert bool(tokens.get('refresh_token'))
