from http import HTTPStatus
from unittest.mock import MagicMock


def test_mail_auth_new_user(mock_get_user_info, mock_authorize_access_token, client):
    test_user_data = dict(
        first_name='Alex',
        last_name='Ivanov',
        email='alex@mail.ru',
        id='57868543',
    )
    token_data = dict(
        access_token='sdfhgdhfdgfghrfgd452345',
        refresh_token='sdfhfgh256778245346342346',
    )

    mock_authorize_access_token.return_value = MagicMock(status_code=200, return_value=token_data)
    mock_authorize_access_token.return_value = token_data
    mock_get_user_info.return_value = MagicMock(status_code=200)
    mock_get_user_info.return_value.json.return_value = test_user_data

    response = client.get('/mail/login')
    assert response.status_code == HTTPStatus.FOUND

    response = client.get('/mail/authorize')
    tokens = response.json

    assert response.status_code == HTTPStatus.OK
    assert bool(tokens.get('access_token'))
    assert bool(tokens.get('refresh_token'))


def test_mail_social_id_not_found(mock_get_user_info, mock_authorize_access_token, client):
    test_user_data = dict(
        first_name='Alex',
        last_name='Ivanov',
        email='alex@mail.ru',
    )
    token_data = dict(
        access_token='sdfhgdhfdgfghrfgd452345',
        refresh_token='sdfhfgh256778245346342346',
    )
    mock_authorize_access_token.return_value = MagicMock(status_code=200, return_value=token_data)
    mock_authorize_access_token.return_value = token_data
    mock_get_user_info.return_value = MagicMock(status_code=200)
    mock_get_user_info.return_value.json.return_value = test_user_data
    response = client.get('/mail/authorize')
    assert response.status_code == HTTPStatus.BAD_GATEWAY
