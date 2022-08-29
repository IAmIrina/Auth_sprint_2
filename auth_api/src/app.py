from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from api.v1.check_roles import CheckRoles
from api.v1.login import Login, Logout, Refresh
from api.v1.password import Password
from api.v1.profile import Profile
from api.v1.roles import Roles, RolesUser
from api.v1.socials.google import google
from api.v1.socials.vk import vkontakte
from api.v1.socials.yandex import yandex
from api.v1.socials.mail import mail
from api.v1.user import UserActivity
from core import config
from core.commands import create_superuser
from core.pagination import pagination
from core.settings import settings
from core.socials.oauth import oauth
from db import redis
from db.storage import db
from swager.config import TEMPLATE
from utils.authentication import jwt

migrate = Migrate()
swagger = Swagger(template=TEMPLATE)


def create_app(config=config.DefaultConfig):

    app = Flask(__name__)
    api = Api(app)
    swagger.init_app(app)
    app.config.from_object(config)
    app.cli.add_command(create_superuser)
    redis.client.init_app(app)
    db.init_app(app)

    from models import user

    migrate.init_app(app, db)
    oauth.init_app(app)
    pagination.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(vkontakte)
    app.register_blueprint(google)
    app.register_blueprint(yandex)
    app.register_blueprint(mail)
    api.add_resource(Login, '/login')
    api.add_resource(Profile, '/user/profile')
    api.add_resource(Logout, '/logout')
    api.add_resource(Refresh, '/refresh')
    api.add_resource(Password, '/change/password')
    api.add_resource(Roles, '/roles', '/roles/<uuid:role_id>')
    api.add_resource(UserActivity, '/user/user_history')
    api.add_resource(CheckRoles, '/user/check_roles')

    api.add_resource(RolesUser, '/users/<uuid:user_id>/roles', '/users/<uuid:user_id>/roles/<uuid:role_id>')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host=settings.host, port=settings.port)