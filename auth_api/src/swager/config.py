from swager.components import components
from swager.roles import (
  roles,
  roles_by_role_id,
  roles_by_user_id,
  roles_by_user_id_and_role_id,
)
from swager.oauth import (
  oauth2_mail_login,
  oauth2_yandex_login,
  oauth2_vk_login,
  oauth2_google_login,
)

TEMPLATE = {
  "swagger": "2.0",
  "info": {
    "title": "Cервис авторизации",
    "description": "Cервис авторизации",
    "version": "0.0.1",
  },
  "securityDefinitions": {
    "Bearer": {
      "type": "apiKey",
      "name": "Authorization",
      "in": "header",
      "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\". In the input enter the following text: Bearer {access_token}."
    },
    "BasicAuth": {"type": "basic"},
    "OAuth2Mail": {
      "type": "oauth2",
      "description": "OAuth2 mail",
      "flow": "accessCode",
      "authorizationUrl": "https://oauth.mail.ru/login",
      "tokenUrl": "https://oauth.mail.ru/token",
      "scopes": {
              "userinfo": "Get information about user"
      }
    },
   "OAuth2Yandex": {
      "type": "oauth2",
      "description": "OAuth2 yandex",
      "flow": "accessCode",
      "authorizationUrl": 'https://oauth.yandex.ru/authorize',
      "tokenUrl": 'https://oauth.yandex.ru/token',
      "scopes": {
              "login:info": "Get info about user",
              "login:email": "Get user emails",
      }
    },
    "OAuth2Vk": {
      "type": "oauth2",
      "description": "OAuth2 vk",
      "flow": "accessCode",
      "authorizationUrl": 'https://oauth.vk.com/authorize',
      "tokenUrl": 'https://oauth.vk.com/access_token',
      "scopes": {
              "email": "Get user email",
      }
    },
    "OAuth2Google": {
      "type": "oauth2",
      "description": "OAuth2 google",
      "flow": "accessCode",
      "authorizationUrl": 'https://accounts.google.com/o/oauth2/auth',
      "tokenUrl": 'https://accounts.google.com/o/oauth2/token',
      "scopes": {
              "openid": "OpenID",
              "email": "Get user email",
              "profile": "Get user profile",
      }
    }
  },
  "security": [
    {
      "Bearer": []
    }
  ],
  "definitions": components,
  "paths": {
      "/roles/{role_id}": roles_by_role_id,
      "/roles": roles,
      "/users/{user_id}/roles/{role_id}": roles_by_user_id_and_role_id,
      "/users/{user_id}/roles": roles_by_user_id,
      "/mail/login": oauth2_mail_login,
      "/yandex/login": oauth2_yandex_login,
      "/vk/login": oauth2_vk_login,
      "/google/login": oauth2_google_login,
  }
}
