"""ABC classes for Oauth."""
from abc import ABC, abstractmethod

from core.socials.social_auth import SocialUser


class OauthServiceProvider(ABC):
    """Provide register data for OAuth provider and parse user info."""
    @property
    @abstractmethod
    def name(self):
        pass

    @staticmethod
    @abstractmethod
    def parse_user_info(user_info: dict, token: dict) -> SocialUser:
        pass

    @abstractmethod
    def get_params(self):
        pass
