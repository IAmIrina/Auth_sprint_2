import click
from db.storage import db
from flask.cli import with_appcontext
from models.user import Role
from schemas.profile import UserSchema


@click.command(name="create_superuser")
@click.argument("password")
@click.argument("email")
@with_appcontext
def create_superuser(password: str, email: str):
    role_name = 'Admin'
    user_schema = UserSchema()
    register = {
        "email": email,
        "password": password,
    }
    user = user_schema.load(register)
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        role = Role(name=role_name)
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()
