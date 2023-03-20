# Query the range
import logging
from src.data_loader.osm_redis import *
from src.graph.road_graph import *
import src.database

class Rangefinder:
    def __init__(self, graph):
        self.logger = logging.getLogger(__name__)
        self.graph = graph
        self.redis_database = src.database.redis_database

    def find_range(self, type, lat, lon, distance):
        query_result = self.redis_database.search_geo(type, lat, lon, distance)
        return list(query_result.keys())

    # todo change the way of distance backoff
    def find_near(self, type, lat, lon, num):
        result = dict()
        distance = 0
        while len(result) < num:
            distance += 500
            query_result = self.redis_database.search_geo(type, lat, lon, distance)
            result.update(query_result)

        src, src_location = self.redis_database.search_closest("intersection", lat, lon)
        
        timeToPoint = dict()
        for place, location in result.items():
            dst, dst_location = self.redis_database.search_closest("intersection", location[1], location[0])
            route, cost = self.graph.pathfinder.find_route(int(src), int(dst))
            timeToPoint[place] = cost
            
        sorted_points = sorted(timeToPoint.items(), key=lambda item: item[1])[:num]
        result = map(lambda point : point[0], sorted_points)

        return list(result)