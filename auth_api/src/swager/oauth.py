socials_url = {
    "get": {
        "summary": "Авторизация через oauth2 google",
        "tags": ["oauth2"],
        "parameters": [
            {
                    "in": "path",
                    "name": "name",
                    "schema": {"type": "string"},
                    "description": "Require one of tehe next socials: yandex, google, mail, vk"
            }],
        "security": [
            {
                "OAuth2Auth": []
            }
        ],
        "responses": {
            "200": {
                "description": "Oauth2 path",
                "schema": {
                    "$ref": "#/definitions/Tokens"
                }
            }
        }
    }
}
