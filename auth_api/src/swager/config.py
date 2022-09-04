from swager.components import components
from swager.roles import (
  roles,
  roles_by_role_id,
  roles_by_user_id,
  roles_by_user_id_and_role_id,
)
from swager.oauth import socials_url


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
    "Secret_key": {
        "type": "apiKey",
        "name": "Authorization",
        "in": "header",
        "description": "Secret internal key to communicate microservice"
    },
    "BasicAuth": {"type": "basic"},
    "OAuth2Auth": {
      "type": "oauth2",
      "description": "OAuth2",
      "flow": "accessCode",
      "authorizationUrl": 'social authorize url',
      "tokenUrl": 'social authorize token',
      "scopes": {
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
      "/socials/login/{name}": socials_url,
  }
}
