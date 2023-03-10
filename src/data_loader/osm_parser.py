# process the data from open street map
import osmium
import logging
from src.data_loader.road_system import *
from src.graph.road_graph import *

road_system = Road_System()
road_graph = Road_Graph()

class Road_Processer(osmium.SimpleHandler):
    def __init__(self):
        super(Road_Processer, self).__init__()

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

            road = Road(r.id, road_name, r.nodes, road_speedlimit)

            if r_type in linkroad_types:
                road_system.add_linked_road(road)
            elif "junction" in r.tags:
                road_system.add_junction_road(road)
            else:
                road_system.add_named_road(road)

    def way(self, w):
        if "highway" in w.tags:
            self.process_road(w)

class Node_Processer(osmium.SimpleHandler):
    def __init__(self):
        super(Node_Processer, self).__init__()

    def process_intersection(self, n):
        intersection = Intersection(n.id, n.location.lat, n.location.lon)
        road_graph.add_intersection(intersection)

    def node(self, n):
        if n.id in road_system.intersections:
            self.process_intersection(n)


class OSM_Parser:
    def __init__(self, soruce_data):
        self.logger = logging.getLogger(__name__)
        self.data = soruce_data

    # the log enable us to trace the performance using the timestamp
    def load_sample_data(self):
        r_processor = Road_Processer()

        self.logger.info("start extracting street from the data file")
        r_processor.apply_file(self.data)
        self.logger.info("finished extracting street from the data file")

        road_system.combine_named_roads()
        road_system.find_interesection()
        road_system.load_roads(road_graph)

        n_processor = Node_Processer()
        n_processor.apply_file(self.data)

        road_graph.find_neighbours()
        road_graph.fdump()



