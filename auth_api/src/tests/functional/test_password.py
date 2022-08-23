
from http import HTTPStatus

import pytest
from models.user import User
from passlib.hash import pbkdf2_sha256


def test_change_password(client, test_user, authorized_client):
    """Change password."""
    new_password = 'fuey47tt4e3e'
    res = client.post(
        "/change/password",
        headers=authorized_client,
        json={
            'old': test_user['password'],
            'new': new_password
        }
    )
    assert res.status_code == HTTPStatus.OK
    user = User.query.get(test_user['id'])
    assert pbkdf2_sha256.verify(new_password, user.password) == True


@pytest.mark.parametrize("new_password",
                         [
                             ('less_10'),
                         ]
                         )
def test_easy_password(new_password, client, test_user, authorized_client):
    """Change password."""
    res = client.post(
        "/change/password",
        headers=authorized_client,
        json={
            'old': test_user['password'],
            'new': new_password
        }
    )
    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
