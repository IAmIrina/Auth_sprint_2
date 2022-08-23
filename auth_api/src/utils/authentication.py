from db.cache_engine import jwt_blocklist, jwt_refresh_cache
from flask_jwt_extended import JWTManager

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    cache_key = jwt_blocklist.gen_cache_key(jti=jti)
    token_in_blacklist = jwt_blocklist.get(cache_key)
    return bool(token_in_blacklist)


@jwt.token_verification_loader
def custom_token_validation(jwt_header, jwt_payload: dict):
    if jwt_payload["type"] != 'refresh':
        return True
    identity = jwt_payload["sub"]
    cache_key = jwt_refresh_cache.gen_cache_key(**identity)

    token = jwt_refresh_cache.get(cache_key)

    return bool(token)
