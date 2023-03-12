# road graph is an abstraction to our road system
import logging

class Node:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon

# our node for the graph
class Intersection(Node):
    def __init__(self, id, lat, lon):
        super().__init__(id, lat, lon)
        self.neighbours = set()

    def add_neighbour(self, n):
        self.neighbours.add(n)

    def __str__(self):
        return "intersection-{}({}, {}), {} neighbours".format(
            str(self.id), str(self.lat), str(self.lon), str(len(self.neighbours)))

# our edge for the graph
class Road_Segment:
    def __init__(self, id, name, src, dst, speed, way_points):
        self.name = name
        self.src = src
        self.dst = dst
        self.speed = speed
        self.points = way_points
    
        self.length = 0
        self.delay = 0

    def __str__(self):
        return "road-{}, {}mph [{}->{}]".format(
            self.name, str(self.speed), str(self.src), str(self.dst))

# our graph
class Road_Graph:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # id to intersection dictionary
        self.intersections = {}
        # src:dst to road_segment dictionary
        self.road_segments = {}
    
    def add_intersection(self, i):
        self.intersections[i.id] = i

    def add_road_segment(self, r):
        r_key = str(r.src) + ":" + str(r.dst)
        self.road_segments[r_key] = r

    #def shortest_path_dijkstra:
        # To implement

    #def shortest_path_astar:
        # To implement

    def find_neighbours(self):
        self.logger.info("start finding neighbours of all the nodes")
        for road_seg in self.road_segments.values():
            self.intersections.get(road_seg.src).add_neighbour(
                self.intersections.get(road_seg.dst))
            self.intersections.get(road_seg.dst).add_neighbour(
                self.intersections.get(road_seg.src))
        self.logger.info("finish finding neighbours of all the nodes")

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