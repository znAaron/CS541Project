# process the data from open street map
import logging
import osmium
from src.data_loader.road_system import *
from src.data_loader.osm_database import *
from src.data_loader.osm_redis import *
from src.graph.road_graph import *
from src.graph.pathfinder import *
import src.database

# define the tags for different road type
road_types = {"motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", "residential"}
linkroad_types = {"motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link"}

road_type_to_speed = {
    "motorway": 70,
    "trunk": 65,
    "primary": 55,
    "secondary": 40,
    "tertiary": 35,
    "unclassified": 25,
    "residential": 25,

    "motorway_link": 55,
    "trunk_link": 45,
    "primary_link": 40,
    "secondary_link": 35,
    "tertiary_link": 30
}

node_delay = {
    "give_way": 5,
    "stop": 10,
    "traffic_signals": 15
}

class Road_Processer(osmium.SimpleHandler):
    def __init__(self, road_system):
        super(Road_Processer, self).__init__()
        self.road_system = road_system

    def process_road(self, r):
        r_type = r.tags.get("highway")
        
        if r_type in road_types or r_type in linkroad_types:
            # process name
            road_name = r.tags.get("name")
            if r_type in linkroad_types:
                road_name = r_type + ":" + str(r.id)
            elif "junction" in r.tags:
                road_name = "junction" + ":" + str(r.id)
            elif road_name is None:
                road_name = "unnamed"

            # process speed
            road_speedlimit = 0
            r_speedlimit = r.tags.get("maxspeed")
            if r_speedlimit is not None:
                try:
                    road_speedlimit = float(r_speedlimit)
                except ValueError:
                    try:
                        road_speedlimit = float(r_speedlimit[:-4])
                    except ValueError:
                        print("error parsing roadspeed: ", r_speedlimit)

            if road_speedlimit == 0:
                road_speedlimit = road_type_to_speed.get(r_type)

            #print(type(r.nodes))
            road = Road(r.id, road_name, r.nodes, road_speedlimit)

            if r_type in linkroad_types:
                self.road_system.add_linked_road(road)
            elif "junction" in r.tags:
                self.road_system.add_junction_road(road)
            else:
                self.road_system.add_named_road(road)

    def way(self, w):
        if "highway" in w.tags:
            self.process_road(w)

class Node_Processer(osmium.SimpleHandler):
    def __init__(self, road_system, road_graph, database, redis):
        super(Node_Processer, self).__init__()
        self.road_graph = road_graph
        self.road_system = road_system
        self.database = database
        self.redis = redis

    def process_intersection(self, n):
        delay = 0
        tag = n.tags.get("highway")
        if tag is not None:
            if tag in node_delay.keys():
                delay = node_delay.get(tag)
        intersection = Intersection(n.id, n.location.lat, n.location.lon, delay)
        self.redis.add_geo("intersection", intersection)
        self.road_graph.add_intersection(intersection)

    def process_interestpoint(self, n):
        amenity_type = n.tags.get("amenity")
        name = n.tags.get("name")
        if amenity_type == "restaurant" or amenity_type == "fast_food" or amenity_type == "food_court":
            point = InterestPoint(n.id, n.location.lat, n.location.lon, name, amenity_type)
            self.redis.add_geo("food", point)

    def node(self, n):
        self.database.insert_node(n.id, n.location.lat, n.location.lon)
        if "amenity" in n.tags:
            self.process_interestpoint(n)
        if n.id in self.road_system.intersections:
            self.process_intersection(n)

class OSM_Parser:
    def __init__(self, soruce_data):
        self.logger = logging.getLogger(__name__)

        self.data = soruce_data
        self.road_system = Road_System()
        self.road_graph = Road_Graph()
        
        self.sql_database = src.database.sql_database
        self.redis_database = src.database.redis_database
        
    # the log enable us to trace the performance using the timestamp
    def load_sample_data(self):
        r_processor = Road_Processer(self.road_system)

        self.logger.info("start extracting street from the data file")
        r_processor.apply_file(self.data)
        self.logger.info("finish extracting street from the data file")

        self.road_system.combine_named_roads()
        self.road_system.find_interesection()
        self.road_system.load_roads(self.road_graph)

        self.logger.info("start extracting node from the data file")
        n_processor = Node_Processer(self.road_system, self.road_graph, self.sql_database, self.redis_database)
        n_processor.apply_file(self.data)
        self.sql_database.flush_node()
        self.logger.info("finish extracting node from the data file")
        
        # preprocessing for the graph
        self.road_graph.process_neighbours()
        self.road_graph.process_distance(self.sql_database)

        return self.road_graph
