
from http import HTTPStatus


def test_get_user_history(client, test_user_history, authorized_client):
    """Get profile log."""
    res = client.get(
        "/user/user_history?device=pc", headers=authorized_client)
    assert res.status_code == HTTPStatus.OK
    res = res.json
    log = res['results']
    assert len(log) == 1
    assert log[0]['browser'] == test_user_history['browser']


def test_get_user_history_other_device(client, authorized_client):
    """Get profile log with OTHER device."""
    res = client.get(
        "/user/user_history?device=other", headers=authorized_client)
    assert res.status_code == HTTPStatus.OK
    res = res.json
    log = res['results']
    assert len(log) == 0


def test_get_user_history_without_authorization(client, test_user_history, authorized_client):
    """Get history info without Autorization."""
    res = client.get(
        "/user/user_history?device=pc")
    assert res.status_code == HTTPStatus.UNAUTHORIZED
