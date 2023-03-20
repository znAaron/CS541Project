# abstract the database interface
import logging
import os
import redis

class OSM_Redis:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # connect to redis database
        # todo: connection pool
        redis_port = os.environ.get('OSM_REDIS_PORT')
        if redis_port is None or os.environ.get('OSM_REDIS_PWD') is None:
            self.logger.error(f"failed to load environment varibles please set them before use")

        self.r = redis.Redis(
            host='localhost',
            port=redis_port,
            password= os.environ.get('OSM_REDIS_PWD'))

    def add_geo(self, type, node):
        self.r.geoadd(type, [node.lon, node.lat, node.name])

    def search_geo(self, type, lat, lon, rad):
        query_result = dict()

        redis_result = self.r.geosearch(type, longitude=lon, latitude=lat, radius=rad, withcoord=True, sort="ASC")
        for result in redis_result:
            query_result[result[0].decode('utf-8')] = result[1]
        return query_result

    def search_closest(self, type, lat, lon):
        redis_result = self.r.geosearch(type, longitude=lon, latitude=lat, radius=500, withcoord=True, sort="ASC", count=1)
        closest_result = redis_result[0]
        closest_result[0] = closest_result[0].decode('utf-8')
        return closest_result[0], closest_result[1]