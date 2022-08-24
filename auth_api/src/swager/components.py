components = {
    "PersonalData": {
        "type": "object",
        "properties": {
            "first_name": {
                "type": "string",
            },
            "second_name": {
                "type": "string"
            },
        },
    },
    "Roles": {
          "type": "object",
          "properties": {
              "id": {
                  "type": "string"
              },
              "name": {
                  "type": "string"
              }
          }
    },
    "ProfileUserSchema": {
          "type": "object",
          "properties": {
              "id": {"type": "string"},
              "email": {"type": "string"},
              "personal_data": {
                    "$ref": "#/definitions/PersonalData"
              },
                "roles": {
                  "type": "array",
                  "items": {
                      "$ref": "#/definitions/Roles"
                  }
              },
          }
      },
    "UserRegisterSchema": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
            },
            "password": {
                "type": "string",
            },
        "personal_data": {
            "$ref": "#/definitions/PersonalData"
        }
      }
    },
    "ChangeProfile": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
            },
            "password": {
                "type": "string",
            },
        "personal_data": {
            "$ref": "#/definitions/ChangePersonalData"
            }
        }
    },
    "ChangePersonalData": {
        "type": "object",
        "properties": {
            "first_name": {
                "type": "string",
            },
            "second_name": {
                "type": "string"
            },
            "example": {"first_name": "Alex", "second_name": "Ivanov"}
        }
    },
    "History": {
        "type": "object",
            "properties": {
                "browser": {"type": "string"},
                "date": {"type": "string"}
        },
    },
    "PaginatedHistory": {
            "type": "object",
            "properties": {
                 "results": {
          "type": "array",
          "items": {"$ref": "#/definitions/History"}
        },
            "current_pae":{"type": "integer"},
            "pages":{"type": "integer"},
            "per_page":{"type": "integer"},

        }
    },
    "PaginatedRoles": {
            "type": "object",
            "properties": {
                 "results": {
          "type": "array",
          "items": {"$ref": "#/definitions/Roles"}
        },
        "current_pae":{"type": "integer"},
        "pages":{"type": "integer"},
        "per_page":{"type": "integer"},

            }
        },
    "PasswordChange": {
            "type": "object",
            "properties": {
                "old": {
                    "type": "string",
                },
                "new": {
                    "type": "string",
                },
            },
        },
    "Login": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
            },
            "password": {
                "type": "string",
            },
        },
    },
    "Tokens": {
        "type": "object",
        "properties": {
            "refresh_token": {
                "type": "string",
            },
            "access_token": {
                "type": "string",
            },
        },
    },
    "AccessToken": {
            "type": "object",
            "properties": {
                "access_token": {
                    "type": "string",
                },
            },
        },
    "RoleList": {
            "type": "object",
            "properties": {
                "roles": {
                  "type": "array",
                  "items": {
                      "$ref": "#/definitions/Roles"
                  }
                },
            }
        }
}





