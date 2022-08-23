from http import HTTPStatus

import pytest


def test_get_roles(client, admin_user, subscriber_role):
    """Get roles by admin"""
    res = client.get(
        "/roles", headers=admin_user)
    assert res.status_code == HTTPStatus.OK
    response = res.json
    roles = res.json['results']
    assert roles[0]['name'] == 'Admin'
    assert len(roles) == 2
    assert response['current_page'] == 1
    assert response['pages'] == 1


def test_get_roles_forbidden(client, authorized_client):
    """Get roles by usual user"""
    res = client.get(
        "/roles", headers=authorized_client)
    assert res.status_code == HTTPStatus.FORBIDDEN


def test_create_roles(client, admin_user, subscriber_role):
    """Create  by admin"""
    res = client.post(
        "/roles",
        json={
            'name': 'Test'
        },
        headers=admin_user)
    assert res.status_code == HTTPStatus.CREATED
    role = res.json
    assert role['name'] == 'Test'
    assert role.get('id') is not None


@pytest.mark.parametrize("name",
                         [
                             ('',),
                             (None, ),
                         ]
                         )
def test_create_role_empty_name(name, client, admin_user, subscriber_role):
    """Create with empty name by admin"""
    res = client.post(
        "/roles",
        json={
            'name': name
        },
        headers=admin_user)
    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_role_forbidden(client, authorized_client):
    """Forbidden to create roles by usual user"""
    res = client.post(
        "/roles", json={
            'name': 'Test'
        },
        headers=authorized_client)
    assert res.status_code == HTTPStatus.FORBIDDEN


def test_delete_role(client, admin_user, subscriber_role):
    """Forbidden to create roles by usual user"""
    res = client.delete(
        f"/roles/{subscriber_role['id']}",
        headers=admin_user)
    assert res.status_code == HTTPStatus.NO_CONTENT


def test_delete_role_forbidden(client, authorized_client, subscriber_role):
    """Forbidden to delete roles by usual user"""
    res = client.delete(
        f"/roles/{subscriber_role['id']}",
        headers=authorized_client)
    assert res.status_code == HTTPStatus.FORBIDDEN
