from core.config import DefaultConfig
from db.cache import Cache
from db.redis import client

jwt_refresh_cache = Cache(client, ttl=DefaultConfig.JWT_REFRESH_TOKEN_EXPIRES, prefix='refresh')
jwt_blocklist = Cache(client, ttl=DefaultConfig.JWT_ACCESS_TOKEN_EXPIRES, prefix='block')
jwt_refresh_blocklist = Cache(client, ttl=DefaultConfig.JWT_REFRESH_TOKEN_EXPIRES, prefix='block')
