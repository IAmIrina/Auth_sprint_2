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


@ pytest.mark.parametrize("email, first_name, second_name",
                          [
                              ('spiderman1@domen.ru', 'Tom', 'Holland'),
                              ('spiderman2@domen.ru', '', ''),
                          ]
                          )
def test_change_profile(email, first_name, second_name, client, test_user, authorized_client):
    """Change profile info."""
    res = client.patch(
        "/user/profile",
        headers=authorized_client,
        json={
            'email': email,
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
    assert profile.get('email') == test_user['email']
    assert personal_data.get('first_name') == first_name
    assert personal_data.get('second_name') == second_name
    assert personal_data.get('passwors') is None
