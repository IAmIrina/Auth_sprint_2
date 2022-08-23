import redis


class RedisCache(redis.Redis):

    def __init__(self):
        pass

    def init_app(self, app):
        super().__init__(
            host=app.config['CACHE_HOST'],
            port=app.config['CACHE_PORT'],
            password=app.config['CACHE_PASSWORD'],
            db=0
        )


client = RedisCache()
