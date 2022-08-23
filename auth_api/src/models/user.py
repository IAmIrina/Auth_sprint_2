import uuid
from datetime import datetime

from db.storage import db
from sqlalchemy.dialects.postgresql import UUID

user_role = db.Table(
    'user_role',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id')),
    db.Column('role_id', UUID(as_uuid=True), db.ForeignKey('role.id')),
)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_joined = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    personal_data = db.relationship('UserPersonalData', backref='user', uselist=False, lazy='joined')
    roles = db.relationship('Role', secondary=user_role, back_populates='users', lazy='joined')
    history = db.relationship('UserHistory', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.login}>'


class UserPersonalData(db.Model):
    __tablename__ = 'user_personal_data'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), unique=True)
    first_name = db.Column(db.String)
    second_name = db.Column(db.String)
    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'User details {self.first_name} {self.second_name}'


class UserHistory(db.Model):
    __tablename__ = 'user_history'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    browser = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'User history {self.id}'


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    users = db.relationship('User', secondary=user_role, back_populates='roles', lazy='dynamic')

    def __repr__(self):
        return f'Role {self.name}'
