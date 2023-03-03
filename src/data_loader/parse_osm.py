# process the data from open street map
import osmium
from road_system import *
from road_graph import *

DATA_FILE = "../../data/osm-sm/west_lafayette.osm"
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
                road_speedlimit = int(r_speedlimit[:-4])

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

r_processor = Road_Processer()
r_processor.apply_file(DATA_FILE)

road_system.combine_named_roads()
road_system.find_interesection()
road_system.load_roads(road_graph)

n_processor = Node_Processer()
n_processor.apply_file(DATA_FILE)

road_graph.fdump()
