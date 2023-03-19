# abstract the database interface
import logging
import os
import redis


class OSM_Redis:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # connect to redis database
        redis_port = os.environ.get('OSM_REDIS_PORT')
        if redis_port is None or os.environ.get('OSM_REDIS_PWD') is None:
            self.logger.error(f"failed to load environment varibles please set them before use")

        self.r = redis.Redis(
            host='localhost',
            port=redis_port,
            password= os.environ.get('OSM_REDIS_PWD'))

    def add_geo(self, type, InterestPoint):
        self.r.geoadd(type, [InterestPoint.lon, InterestPoint.lat, InterestPoint.name])