from http import HTTPStatus

import pytest


def test_get_profile(client, test_user, test_user2, authorized_client):
    """Get profile info."""
    res = client.get(
        "/user/profile", headers=authorized_client)
    assert res.status_code == HTTPStatus.OK
    user = res.json
    test_user.pop('password')
    assert user == test_user


def test_get_profile_no_auth(client, test_user, authorized_client):
    """Get profile info without Autorization."""
    res = client.get(
        "/user/profile")
    assert res.status_code == HTTPStatus.UNAUTHORIZED


@ pytest.mark.parametrize("login, first_name, second_name",
                          [
                              ('Spiderman', 'Tom', 'Holland'),
                              ('Spiderman', '', ''),
                          ]
                          )
def test_change_profile(login, first_name, second_name, client, test_user, authorized_client):
    """Change profile info."""
    res = client.patch(
        "/user/profile",
        headers=authorized_client,
        json={
            'login': login,
            'personal_data': {
                'first_name': first_name,
                'second_name': second_name,
            }
        }
    )
    assert res.status_code == HTTPStatus.OK

    profile = res.json
    personal_data = profile.get('personal_data') if profile.get('personal_data') else {}
    assert profile.get('id') == test_user['id']
    assert profile.get('login') == login
    assert personal_data.get('email') == personal_data['email']
    assert personal_data.get('first_name') == first_name
    assert personal_data.get('second_name') == second_name
    assert personal_data.get('passwors') is None


@ pytest.mark.parametrize("login",
                          [
                              (''),
                              (None),
                          ]
                          )
def test_change_profile_empty_login(login, client, test_user, authorized_client):
    """Clean login."""
    res = client.patch(
        "/user/profile",
        headers=authorized_client,
        json={
            'login': login,
        }
    )
    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
