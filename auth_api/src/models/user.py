import uuid
from datetime import datetime

from passlib.hash import pbkdf2_sha256
from db.storage import db
from core.constants import DEVICES
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property


user_role = db.Table(
    'user_role',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id')),
    db.Column('role_id', UUID(as_uuid=True), db.ForeignKey('role.id')),
)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    date_joined = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    personal_data = db.relationship('UserPersonalData', backref='user', uselist=False, lazy='joined')
    roles = db.relationship('Role', secondary=user_role, back_populates='users', lazy='joined')
    history = db.relationship('UserHistory', backref='user', lazy='dynamic')
    social_accounts = db.relationship('SocialAccount', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return f'<User {self.login}>'

    @hybrid_property
    def password(self) -> str:
        """Return the hashed user password."""
        return self.password_hash

    @password.setter
    def password(self, password) -> str:
        """Hashed password."""
        self.password_hash = pbkdf2_sha256.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify password."""
        return pbkdf2_sha256.verify(password, self.password_hash)


class UserPersonalData(db.Model):
    __tablename__ = 'user_personal_data'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), unique=True)
    first_name = db.Column(db.String)
    second_name = db.Column(db.String)

    def __repr__(self):
        return f'User details {self.first_name} {self.second_name}'


class SocialAccount(db.Model):
    __tablename__ = 'social_account'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)

    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint('social_id', 'social_name', name='social_pk'), )

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'


def create_partition(target, connection, **kw) -> None:
    """Creating partition by user_history."""
    table = 'user_history'
    query = """CREATE TABLE IF NOT EXISTS {partition} PARTITION OF {table} FOR VALUES IN ('{device}')"""
    for device in DEVICES:
        stmt = query.format(
            partition=f'{table}_{device}',
            table=table,
            device=device,
        )
        connection.execute(stmt)


class UserHistory(db.Model):
    __tablename__ = 'user_history'
    __table_args__ = (
        UniqueConstraint('id', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_device_type)',
            'listeners': [('after_create', create_partition)],
        }
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    browser = db.Column(db.String, nullable=False)
    logged_in_at = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    user_device_type = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        return f'User_history {self.id}'


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    users = db.relationship('User', secondary=user_role, back_populates='roles', lazy='dynamic')

    def __repr__(self):
        return f'Role {self.name}'
