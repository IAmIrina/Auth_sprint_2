from http import HTTPStatus

import pytest
from flask_jwt_extended import decode_token


@pytest.mark.parametrize("login, password, email, first_name, second_name",
                         [
                             ('Spiderman', '48y73t4rr6t', 'tholland@google.com', 'Tom', 'Holland'),
                             ('Spiderman', '48y73t4rr6t', 'tholland@google.com', '', ''),
                         ]
                         )
def test_register(client, login, password, email, first_name, second_name):
    """Create new user."""
    res = client.post(
        '/user/profile',
        json={
            'login': login,
            'password': password,
            'personal_data': {
                'email': email,
                'first_name': first_name,
                'second_name': second_name,
            }
        }
    )
    new_user = res.json
    personal_data = new_user.get('personal_data') if new_user.get('personal_data') else {}
    assert new_user.get('id') is not None
    assert personal_data.get('email') == email
    assert personal_data.get('first_name') == first_name
    assert personal_data.get('second_name') == second_name
    assert personal_data.get('passwors') is None
    assert res.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize("login, password, email, first_name, second_name",
                         [
                             ('', '48y73t4rr6t', 'tholland@google.com', 'Tom', 'Holland'),
                             (None, '48y73t4rr6t', 'tholland@google.com', 'Tom', 'Holland')
                         ]
                         )
def test_no_login_register(client, login, password, email, first_name, second_name):
    """Create new user."""
    res = client.post(
        '/user/profile',
        json={
            'login': login,
            'password': password,
            'personal_data': {
                'email': email,
                'first_name': first_name,
                'second_name': second_name,
            }
        }
    )
    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_login_user(client, test_user):
    """Login endpoint."""
    res = client.post(
        "/login", auth=(test_user["login"], test_user["password"]))

    assert res.status_code == HTTPStatus.OK
    access_token = res.json.get('access_token')
    refresh_token = res.json.get('refresh_token')

    access_token = decode_token(access_token)
    assert access_token.get('fresh') == True
    assert access_token.get('type') == 'access'

    access_user_token_info = access_token.get('sub')
    assert access_user_token_info.get('id') == test_user['id']

    refresh_token = decode_token(refresh_token)
    assert refresh_token.get('type') == 'refresh'

    refresh_user_token_info = refresh_token.get('sub')
    assert refresh_user_token_info.get('id') == test_user['id']


def test_wrong_password(client, test_user):
    """Wrong password login."""
    res = client.post(
        "/login", auth=(test_user["login"], 'WRONG_PASSWORD'))
    assert res.status_code == HTTPStatus.UNAUTHORIZED


def test_logout(client, authorized_client):
    """Logout."""
    res = client.delete(
        "/logout", headers=authorized_client)
    assert res.status_code == HTTPStatus.NO_CONTENT


def test_revoked_token(client, revoked_client_token):
    """Try to use revoked token."""
    res = client.post(
        "/login", headers=revoked_client_token)

    assert res.status_code == HTTPStatus.UNAUTHORIZED


def test_refresh(client, test_user, tokens):
    """Refresh tokens."""
    header = {"Authorization": f"Bearer {tokens[1]['refresh_token']}"}
    res = client.post(
        "/refresh", headers=header)
    assert res.status_code == HTTPStatus.OK

    access_token = res.json.get('access_token')
    refresh_token = res.json.get('refresh_token')
    access_token = decode_token(access_token)
    assert access_token.get('fresh') == False
    assert access_token.get('type') == 'access'

    access_user_token_info = access_token.get('sub')
    assert access_user_token_info.get('id') == test_user['id']

    refresh_token = decode_token(refresh_token)
    assert refresh_token.get('type') == 'refresh'

    refresh_user_token_info = refresh_token.get('sub')
    assert refresh_user_token_info.get('id') == test_user['id']
