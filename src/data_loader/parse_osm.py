# process the data from open street map

import osmium
from road_system import *

DATA_FILE = "../../data/osm-sm/west_lafayette.osm"
road_system = Road_System()

class Data_Processer(osmium.SimpleHandler):
    def __init__(self):
        super(Data_Processer, self).__init__()

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

processor = Data_Processer()
processor.apply_file(DATA_FILE)

road_system.combine_named_roads()
road_system.find_interesection()
for road in road_system.processed_roads:
    print(road)
