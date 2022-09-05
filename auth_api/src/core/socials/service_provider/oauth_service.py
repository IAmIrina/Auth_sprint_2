"""ABC classes for Oauth."""
from abc import ABC, abstractmethod

from core.socials.social_auth import SocialUser


class OauthServiceProvider(ABC):
    """Provide register data for OAuth provider and parse user info."""
    @property
    @abstractmethod
    def name(self):
        """Service provider name."""
        pass

    @staticmethod
    @abstractmethod
    def parse_user_info(user_info: dict, token: dict) -> SocialUser:
        """Transform user info to approptiate format."""
        pass

    @staticmethod
    def get_userinfo_params(**kwargs) -> dict:
        """Dinamic request params for userinfo endpoint."""
        return {}

    @abstractmethod
    def get_params(self) -> dict:
        """Service provider settings."""
        pass
