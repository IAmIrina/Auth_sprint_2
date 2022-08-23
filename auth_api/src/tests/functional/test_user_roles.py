from http import HTTPStatus


def test_add_roles(client, admin_user, test_user2, subscriber_role):
    """Add roles."""
    res = client.post(
        f"/users/{test_user2['id']}/roles/{subscriber_role['id']}", headers=admin_user)
    assert res.status_code == HTTPStatus.OK
    roles = res.json
    assert roles[0]['name'] == subscriber_role['name']
    assert len(roles) == 1


def test_get_roles(client, admin_user, test_user):
    """Get roles."""
    res = client.get(
        f"/users/{test_user['id']}/roles", headers=admin_user)
    assert res.status_code == HTTPStatus.OK
    roles = res.json
    assert roles[0]['name'] == 'Admin'
    assert len(roles) == 1


def test_delete_role(client, admin_user, subscriber, subscriber_role):
    """Delete roles."""
    res = client.delete(
        f"/users/{subscriber['id']}/roles/{subscriber_role['id']}", headers=admin_user)
    assert res.status_code == HTTPStatus.NO_CONTENT
