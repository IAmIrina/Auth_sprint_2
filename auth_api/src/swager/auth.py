login = {
  "summary":  "Вход пользователя",
  "tags": ["auth"],
  "security": [
    {
      "BasicAuth": []
    }
  ],
    "responses": {
    "200": {
      "description": "Токены пользователя",
      "schema": {
        "$ref": "#/definitions/Tokens"
      }
    }
  }
}

logout = {
"summary":  "Выход пользователя",
  "tags": ["auth"],
    "responses": {
    "200": {
      "description": "{type} token successfully revoked",
    }
  }
}

refresh = {
    "summary":  "Обновление токенов",
    "tags": ["auth"],
    "responses": {
    "200": {
      "description": "Токены успешно обновлены",
      "schema": {
        "$ref": "#/definitions/Tokens"
      }
    }
  }
}

change_password = {
    "summary": "Изменение пароля",
    "tags": ["auth"],
    "parameters": [
        {
            "name": "passwords",
            "in": "body",
            "schema": {"$ref": "#/definitions/PasswordChange"},
            "required": "true",
        }
    ],
    "responses": {
        "200": {
            "description": "Password has been successfully changed.",
        }
    }
}