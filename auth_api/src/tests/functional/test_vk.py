from http import HTTPStatus
from unittest.mock import MagicMock


def test_vk_auth_new_user(mock_get_user_info, mock_authorize_access_token, client):
    """VK OAuth for new user."""
    test_user_data = dict(
        email='bp@gmail.com',
        user_id='id_12345678',
    )
    test_user_data = {
        'response': [test_user_data]
    }
    token_data = dict(
        first_name='Brad',
        last_name='Pitt',
    )

    mock_authorize_access_token.return_value = MagicMock(status_code=200, return_value=token_data)
    mock_authorize_access_token.return_value = token_data
    mock_get_user_info.return_value = MagicMock(status_code=200)
    mock_get_user_info.return_value.json.return_value = test_user_data

    response = client.get('/vk/login')
    assert response.status_code == HTTPStatus.FOUND

    response = client.get('/vk/authorize')
    tokens = response.json

    assert response.status_code == HTTPStatus.OK
    assert bool(tokens.get('access_token'))
    assert bool(tokens.get('refresh_token'))


def test_vk_auth_user_already_exists(mock_get_user_info, mock_authorize_access_token, client, test_user):
    """VK OAuth for registered user."""
    test_user_data = dict(
        email=test_user['email'],
        social_id='id_12345678',
    )
    test_user_data = {
        'response': [test_user_data]
    }
    token_data = dict(
        first_name=test_user['personal_data']['first_name'],
        last_name=test_user['personal_data']['second_name'],
    )
    mock_authorize_access_token.return_value = MagicMock(status_code=200)
    mock_authorize_access_token.return_value = token_data
    mock_get_user_info.return_value = MagicMock(status_code=200)
    mock_get_user_info.return_value.json.return_value = test_user_data

    response = client.get('/vk/login')
    assert response.status_code == HTTPStatus.FOUND

    response = client.get('/vk/authorize')
    tokens = response.json

    assert response.status_code == HTTPStatus.OK
    assert bool(tokens.get('access_token'))
    assert bool(tokens.get('refresh_token'))
