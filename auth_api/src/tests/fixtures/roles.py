import pytest
from app import db
from models.user import Role, User
from schemas.roles import RoleSchema


@pytest.fixture
def subscriber_role(client):
    role_data = {
        'name': 'Subscriber',
    }
    role = Role(**role_data)
    db.session.add(role)
    db.session.commit()
    role = RoleSchema().dump(role)
    return {**role}


@pytest.fixture
def admin_role(client):
    role_data = {
        'name': 'Admin',
    }
    role = Role(**role_data)
    db.session.add(role)
    db.session.commit()
    role = RoleSchema().dump(role)
    return {**role}


@pytest.fixture
def admin_user(test_user, admin_role, authorized_client):
    user = User.query.filter_by(id=test_user['id']).first()
    role = Role.query.filter_by(id=admin_role['id']).first()
    user.roles.append(role)
    db.session.commit()
    return authorized_client


@pytest.fixture
def subscriber(test_user2, subscriber_role):
    user = User.query.filter_by(id=test_user2['id']).first()
    role = Role.query.filter_by(id=subscriber_role['id']).first()
    user.roles.append(role)
    db.session.commit()
    return test_user2
