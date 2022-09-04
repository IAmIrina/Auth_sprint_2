from core.constants import DEVICES

user_register = {
  "summary":  "Регистрация пользователя",
  "tags": ["profile"],
    "parameters": [
        {
            "name": "profile_info",
            "in": "body",
            "schema": {"$ref": "#/definitions/UserRegisterSchema"},
            "required": "true",
        }
    ],
    "security": [],
  "responses": {
    "201": {
      "description": "Информация оп пользователе",
      "schema": {
        "$ref": "#/definitions/ProfileUserSchema"
      }
    }
  }
}

user_change_schema = {
  "summary":  "Изменения профиля пользователя",
  "tags": ["profile"],
    "parameters": [
        {
            "name": "profile_info",
            "in": "body",
            "schema": {"$ref": "#/definitions/ChangeProfile"},
            "required": "true",
        }
    ],
  "responses": {
    "200": {
      "description": "Profile info",
      "schema": {
        "$ref": "#/definitions/ProfileUserSchema"
      }
    }
  }
}

get_user_info = {
  "summary":  "Информация о профиле",
  "tags": ["profile"],
  "responses": {
    "200": {
      "description": "Информация о пользователе",
      "schema": {
        "$ref": "#/definitions/ProfileUserSchema"
      }
    }
  }
}

user_history = {
    "summary": "История активности пользователя",
    "tags": ["profile"],
    "parameters": [
        {
            "in": "query",
            "name": "device",
            "schema": {"type": "string"},
            "description":  f"Required device type: {','.join(DEVICES)}"
        },
        {
            "in": "query",
            "name": "page",
            "schema": {"type": "integer"},
            "description":  "Page number"
        },
        {
            "in": "query",
            "name": "size",
            "schema": {"type": "integer"},
            "description": "Page size",
        }
    ],
    "responses": {
        "200": {
                "description": "Список ролей пользователя",
                "schema": {"$ref": "#/definitions/PaginatedHistory"}
        }
    }
}

check_roles = {
    "summary": "Список ролей у пользователя",
    "tags": ["user_role"],
    "security": [
        {
            "Secret_key": []
        }
    ],
    "parameters": [
        {
            "name": "token",
            "in": "body",
            "schema": {"$ref": "#/definitions/AccessToken"},
            "required": "true",
        }
    ],
    "responses": {
        "200": {
            "description": "Список ролей пользователя",
            "schema": {"$ref": "#/definitions/RoleList"}
        }
    }
}