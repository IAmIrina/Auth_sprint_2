import pytest
from app import db
from core.access import create_token_pair
from models.user import User, UserPersonalData
from passlib.hash import pbkdf2_sha256
from schemas.profile import UserSchema


@pytest.fixture
def test_user(client):
    user_data = {
        'email': 'Nickname@domen.ru',
        'password': '1uer84r3r2345',
    }
    personal_data = {
        'first_name': 'Van',
        'second_name': 'Gog',
    }
    personal = UserPersonalData(**personal_data)
    user = User(
        email=user_data['email'],
        password=pbkdf2_sha256.hash(
            user_data['password']),
        personal_data=personal)
    db.session.add(user)
    db.session.commit()
    user = UserSchema().dump(user)
    return {**user, 'password': user_data['password']}


@pytest.fixture
def test_user2(client):
    user_data = {
        'email': 'second@user.ru',
        'password': 'yr74r74rte6',
    }
    personal_data = {
        'first_name': 'Wal De',
        'second_name': 'Mort',
    }
    personal = UserPersonalData(**personal_data)
    user = User(
        email=user_data['email'],
        password=pbkdf2_sha256.hash(
            user_data['password']),
        personal_data=personal)
    db.session.add(user)
    db.session.commit()
    user = UserSchema().dump(user)
    return {**user, 'password': user_data['password']}


@pytest.fixture
def tokens(test_user):
    user = User.query.filter_by(id=test_user['id']).first()
    identity, tokens = create_token_pair(user, fresh=True)
    return identity, tokens


@pytest.fixture
def authorized_client(tokens):
    header = {"Authorization": f"Bearer {tokens[1]['access_token']}"}
    return header


@pytest.fixture
def revoked_client_token(client, authorized_client):
    _ = client.delete(
        "/logout", headers=authorized_client)
    return authorized_client
