from http import HTTPStatus

from core.settings import settings


def test_check_roles(client, admin_user, tokens):
    """Get user roles by token."""
    res = client.post(
        "/user/check_roles",
        json={
            'access_token': tokens[1]['access_token']
        },
        headers={'Authorization': settings.async_secret_key})
    assert res.status_code == HTTPStatus.OK
    roles = res.json
    assert roles[0]['name'] == 'Admin'
    assert len(roles) == 1
