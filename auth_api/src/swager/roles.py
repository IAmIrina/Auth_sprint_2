roles_by_role_id = {
    "delete": {
        "summary": "Удаление роли",
        "tags": ["role"],
        "parameters": [
            {
                "in": "path",
                "name": "role_id",
                "schema": {"type": "string"},
                "required": True,
                "description":  "Role id"
            },
        ],
        "responses": {"204": {}}
        },
    "get": {
        "summary": "Получить роль по id",
        "tags": ["role"],
        "parameters": [
            {
            "in": "path",
            "name": "role_id",
            "schema":{"type": "string"},
            "required": True,
            "description":  "Role id"
            },
        ],
        "responses": {
            "200": {
            "description": "Role by id",
            "schema": {
            "$ref": "#/definitions/Roles"
            }
        }
    }
    }
}

roles = {
        "get": {
            "summary": "Список ролей",
            "tags": ["role"],
            "parameters": [
            {
                "in": "query",
                "name": "page",
                "schema":{"type": "integer"},
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
                "201": {
                    "description": "Role list",
                    "schema": {
                        "$ref": "#/definitions/PaginatedRoles"
                    }
                }
            }
        },
        "post": {
            "summary": "Создать роль",
            "tags": ["role"],
            "parameters": [
                {
                    "in": "body",
                    "name": "name",
                    "schema": {"type": "string"},
                    "description": "Role name"
                },
            ],
            "responses": {
                "201": {
                    "description": "Role list",
                    "schema": {
                        "$ref": "#/definitions/Roles"
                    }
            }
        }
    }
}

roles_by_user_id_and_role_id = {
        "post": {
            "summary": "Создать роль",
            "tags": ["user_role"],
            "parameters": [
                {
                    "in": "path",
                    "name": "user_id",
                    "schema": {"type": "string"},
                    "description": "User id"
                },
                {
                    "in": "path",
                    "name": "role_id",
                    "schema": {"type": "string"},
                    "description": "Role id"
                },
            ],
            "responses": {
                "201": {
                    "description": "Role create",
                    "schema": {
                        "$ref": "#/definitions/RoleList"
                    }
                }
            }
        },
        "delete": {
            "summary": "Удалить роль",
            "tags": ["user_role"],
            "parameters": [
                {
                    "in": "path",
                    "name": "user_id",
                    "schema": {"type": "string"},
                    "description": "User id"
                },
                {
                    "in": "path",
                    "name": "role_id",
                    "schema": {"type": "string"},
                    "description": "Role id"
                },
            ],
            "responses": {
                "200": {
                    "description": "Role delete",
                    "schema": {"$ref": "#/definitions/RoleList"}
                }
            }
        }
    }

roles_by_user_id = {
        "get": {
            "summary": "Список ролей пользователя",
            "tags": ["user_role"],
            "parameters": [
                {
                    "in": "path",
                    "name": "user_id",
                    "schema": {"type": "string"},
                    "description": "User id"
                },
            ],
            "responses": {
                "200": {
                    "description": "User role list",
                    "schema": {
                        "$ref": "#/definitions/RoleList"
                    }
                }
            }
        }
    }
