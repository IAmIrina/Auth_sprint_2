from http import HTTPStatus
from unittest.mock import MagicMock


def test_mail_auth_new_user(mock_user_info, mock_authorize_access_token, client):
    test_user_data = dict(
        first_name='Alex',
        last_name='Ivanov',
        email='alex@mail.ru',
        id='57868543',
    )
    mock_authorize_access_token.return_value.status_code = HTTPStatus.OK
    mock_user_info.return_value = test_user_data

    response = client.get('/socials/login/mail')
    assert response.status_code == HTTPStatus.FOUND

    response = client.get('/socials/auth/mail')
    tokens = response.json

    assert response.status_code == HTTPStatus.OK
    assert bool(tokens.get('access_token'))
    assert bool(tokens.get('refresh_token'))


def test_mail_social_id_not_found(mock_user_info, mock_authorize_access_token, client):
    test_user_data = dict(
        first_name='Alex',
        last_name='Ivanov',
        email='alex@mail.ru',
    )
    mock_authorize_access_token.return_value.status_code = HTTPStatus.OK
    mock_user_info.return_value = test_user_data
    response = client.get('/socials/auth/mail')
    assert response.status_code == HTTPStatus.BAD_GATEWAY
