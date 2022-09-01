"""VK Social Login class."""
import string
import uuid
from http import HTTPStatus
from secrets import choice as secrets_choice
from typing import Tuple

from flask_restful import abort

from core.access import create_token_pair
from core.constants import FAKE_MAIL_DOMAIN, PASSWORD_LEN
from core.message_constants import MSG_SOCIAL_NETWORK_ERROR
from utils.parse_user_agent import get_device_type
from db.storage import db
from models.user import SocialAccount, User, UserHistory, UserPersonalData
from utils.model_func import get_user_by_email, get_user_by_social


class SocialAuth():
    """Authorization via socials."""

    def __init__(self, social_name: str) -> None:
        self.social = social_name

    def authorize(
        self,
        social_id: str,
        user_agent: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
    ) -> dict:

        if not social_id:
            abort(HTTPStatus.BAD_GATEWAY, message=MSG_SOCIAL_NETWORK_ERROR)

        user, tokens = self.search_in_social_account(social_id)

        if user:
            self.save_log(user, user_agent)
            return tokens

        if email:
            user, tokens = self.search_in_users(email)
            if user:
                self.save_social_account(user, social_id)
                self.save_log(user, user_agent)
                return tokens
        user, tokens = self.register_user(email=email, first_name=first_name, last_name=last_name)
        self.save_social_account(user, social_id)
        self.save_log(user, user_agent)
        return tokens

    def search_in_social_account(self, social_id: str) -> Tuple[User, dict]:
        user = get_user_by_social(social_id, self.social)
        if not user:
            return None, {}
        _, tokens = create_token_pair(user, fresh=True)
        return user, tokens

    def search_in_users(self, email: str) -> Tuple[User, dict]:
        user = get_user_by_email(email)
        if not user:
            return None, {}
        _, tokens = create_token_pair(user, fresh=True)
        return user, tokens

    def register_user(self, email: str = None, first_name: str = None, last_name: str = None) -> Tuple[User, dict]:
        if not email:
            email = self.generate_email()
        user = User(email=email, password=self.generate_password())
        personal_data = UserPersonalData(first_name=first_name, second_name=last_name)
        user.personal_data = personal_data
        db.session.add(user)
        db.session.commit()
        _, tokens = create_token_pair(user, fresh=True)
        return user, tokens

    def save_social_account(self, user: User, social_id: str) -> None:
        social = SocialAccount(social_id=social_id, social_name=self.social)
        user.social_accounts.append(social)
        db.session.commit()

    def save_log(self, user: User, user_agent: str) -> None:
        user.history.append(UserHistory(browser=user_agent, user_device_type=get_device_type(user_agent)))
        db.session.commit()

    def generate_password(self) -> None:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets_choice(alphabet) for _ in range(PASSWORD_LEN))

    def generate_email(self) -> None:
        login = uuid.uuid4()
        return f'{login}{FAKE_MAIL_DOMAIN}'
