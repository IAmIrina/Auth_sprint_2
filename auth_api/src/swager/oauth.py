oauth2_mail_login = {
        "get": {
            "summary": "Авторизация через oauth2 mail",
            "tags": ["oauth2"],
            "security": [
                {
                    "OAuth2Mail": []
                }
            ],
            "responses": {
                "302": {
                    "description": "Redirect url /mail/authorize",
                        "schema": {
                            "$ref": "#/definitions/Tokens"
                    }
                }
            }
        }
    }

oauth2_yandex_login = {
        "get": {
            "summary": "Авторизация через oauth2 yandex",
            "tags": ["oauth2"],
            "security": [
                {
                    "OAuth2Yandex": []
                }
            ],
            "responses": {
                "302": {
                    "description": "Redirect url /yandex/authorize",
                        "schema": {
                            "$ref": "#/definitions/Tokens"
                    }
                }
            }
        }
    }

oauth2_vk_login = {
        "get": {
            "summary": "Авторизация через oauth2 vk",
            "tags": ["oauth2"],
            "security": [
                {
                    "OAuth2Vk": []
                }
            ],
            "responses": {
                "302": {
                    "description": "Redirect url /vk/authorize",
                        "schema": {
                            "$ref": "#/definitions/Tokens"
                    }
                }
            }
        }
    }

oauth2_google_login = {
        "get": {
            "summary": "Авторизация через oauth2 google",
            "tags": ["oauth2"],
            "security": [
                {
                    "OAuth2Google": []
                }
            ],
            "responses": {
                "302": {
                    "description": "Redirect url /google/authorize",
                        "schema": {
                            "$ref": "#/definitions/Tokens"
                    }
                }
            }
        }
    }
