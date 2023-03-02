import osmium

SAMPLE_FILE = "data/osm-sm/west_lafayette.osm"

road_types = {"motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", "residential"}
linkroad_types = {"motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link"}

class Road:
    def __init__(self, id, name, nodes, speedlimit):
        self.id = id
        self.name = name
        self.speedlimit = speedlimit

        self.nodes = []
        for n in nodes:
            self.nodes.append(n)

    def __str__(self):
        return "{" + str(self.id) + ", " + self.name + ", " + str(self.speedlimit) + ", (" + ', '.join(str(x) for x in self.nodes) + ")}"

roads = []

class HotelCounterHandler(osmium.SimpleHandler):
    def __init__(self):
        super(HotelCounterHandler, self).__init__()

        self.num_nodes = 0
        self.fast_foods = []

        self.waypoints = {}
        self.intersections = {}


    def process_road(self, r):
        r_type = r.tags.get("highway")
        
        if r_type in road_types or r_type in linkroad_types:
            # process name
            road_name = r.tags.get("name")
            if r_type in linkroad_types:
                road_name = "link"
            elif "junction" in r.tags:
                road_name = "junction"

            # process speed
            road_speedlimit = r.tags.get("maxspeed")

            road = Road(r.id, 
                road_name, 
                r.nodes, 
                road_speedlimit)
            roads.append(road)

    def node(self, n):
        if n.tags.get("amenity") == "fast_food" and "name" in n.tags:
            self.fast_foods.append(n.tags["name"])

    def way(self, w):
        if "highway" in w.tags:
            self.process_road(w)

    # def relation(self, r):
        # not implemented
        


h = HotelCounterHandler()
h.apply_file(SAMPLE_FILE)

#print("fast food: ", h.fast_foods)
for road in roads:
    print(road)