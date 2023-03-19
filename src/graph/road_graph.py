# road graph is an abstraction to our road system
import logging
from haversine import haversine, Unit
from src.graph.visualizer import *
from src.graph.pathfinder_astar import *

MPH_MS_FACTOR = 0.44704

class Node:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon

    def location(self):
        return(self.lat, self.lon)

# our node for the graph
class Intersection(Node):
    def __init__(self, id, lat, lon, delay):
        super().__init__(id, lat, lon)
        self.neighbours = set()
        self.delay = delay

    def add_neighbour(self, n):
        self.neighbours.add(n)

    def __str__(self):
        return "intersection-{}({}, {}), delay {} s, {} neighbours".format(
            str(self.id), str(self.lat), str(self.lon), str(self.delay), str(len(self.neighbours)))

# our edge for the graph
class Road_Segment:
    def __init__(self, id, name, src, dst, speed, way_points):
        self.name = name
        self.src = src
        self.dst = dst
        self.speed = speed
        self.points = way_points
    
        # length in miles
        self.length = 0
        # delay in seconds
        self.delay = 0

    def process_distance(self, database):
        src_node = database.get_node(self.src)
        prev_node = (src_node.lat, src_node.lon)
        distance = 0
        
        for nid in self.points:
            node = database.get_node(nid)
            curr_node = (node.lat, node.lon)
            subdistance = haversine(prev_node, curr_node, unit=Unit.METERS)
            distance += subdistance
            prev_node = curr_node
        dst_node = database.get_node(self.dst)
        curr_node = (dst_node.lat, dst_node.lon)
        subdistance = haversine(prev_node, curr_node, unit=Unit.METERS)
        distance += subdistance
            
        self.length = distance
        self.delay = self.length / self.speed * MPH_MS_FACTOR

    def __str__(self):
        return "road-{}, length: {}m, speed: {}mph, time: {}s [{}->{}]".format(
            self.name, str(self.length), str(self.speed), str(self.delay), str(self.src), str(self.dst))

# our graph
class Road_Graph:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # id to intersection dictionary
        self.intersections = {}
        # src:dst to road_segment dictionary
        self.road_segments = {}
        # visualize the graph
        self.visualizer = Visualizer(self)
        # find the shortest path
        self.pathfinder = Pathfinder(self)
    
    def add_intersection(self, i):
        self.intersections[i.id] = i

    def add_road_segment(self, r):
        key1 = str(r.src) + ":" + str(r.dst)
        key2 = str(r.dst) + ":" + str(r.src)
        self.road_segments[key1] = r
        self.road_segments[key2] = r

    def delay(self, i1, i2):
        key = str(i1) + ":" + str(i2)
        seg = self.road_segments.get(key)
        dst = self.intersections.get(i2)
        if seg is None or dst is None:
            return 360000
        return seg.delay + dst.delay 

    def harv_distance(self, i1, i2):
        src = self.intersections.get(i1)
        dst = self.intersections.get(i2)
        distance = haversine(src.location(), dst.location(), unit=Unit.METERS)
        return distance

    def route_to_location(self, route):
        locations = []
        for id in route:
            locations.append(self.intersections.get(id).location())
        return locations

    def center_point(self, locations):
        lat_sum = 0
        lon_sum = 0
        num_location = len(locations)
        for location in locations:
            lat_sum += location[0]
            lon_sum += location[1]
        center = (lat_sum/num_location, lon_sum/num_location)

        return center

    #def shortest_path_dijkstra:
        # To implement

    #def shortest_path_astar:
        # To implement

    def process_neighbours(self):
        self.logger.info("start finding neighbours of all the nodes")
        for road_seg in self.road_segments.values():
            self.intersections.get(road_seg.src).add_neighbour(road_seg.dst)
            self.intersections.get(road_seg.dst).add_neighbour(road_seg.src)
        self.logger.info("finish finding neighbours of all the nodes")

    def process_distance(self, database):
        self.logger.info("start calculating distance for the road segments")
        for road_seg in self.road_segments.values():
            road_seg.process_distance(database)
        self.logger.info("finish calculating distance for the road segments")

    # prefer using fdump because the file can get large
    def dump(self):
        self.logger.info("Dumping Road Graph:\n=========================")
        self.logger.info("Intersections:")
        for intersection in self.intersections.values():
            self.logger.info(intersection)
        self.logger.info("\nRoad_Segments:")
        for road_seg in self.road_segments.values():
            self.logger.info(road_seg)

    def fdump(self):
        with open("./output/road_graph_dump.txt", "w") as f:
            f.write("Road Graph:\n=========================")
            f.write("\nIntersections:\n")
            for intersection in self.intersections.values():
                f.write(str(intersection))
                f.write("\n")
            f.write("\nRoad_Segments:\n")
            for road_seg in self.road_segments.values():
                f.write(str(road_seg))
                f.write("\n")