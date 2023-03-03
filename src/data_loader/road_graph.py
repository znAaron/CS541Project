# road graph is an abstraction to our road system

# our node for the graph
class Intersection:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.neighbours = []

    def add_neighbour(n):
        neighbours.append(n)

    def __str__(self):
        return "intersection-{}({}, {})".format(
            str(self.id), str(self.lat), str(self.lon))

# our edge for the graph
class Road_Segment:
    def __init__(self, id, name, src, dst, speed, way_points):
        self.id = id
        self.name = name
        self.src = src
        self.dst = dst
        self.speed = 30
        if speed != 0:
            self.speed = speed
        self.points = way_points

        self.length = 0
        self.delay = 0

    def __str__(self):
        return "road-{}({}), {}mph [{}->{}]".format(
            self.name, str(self.id), str(self.speed), str(self.src), str(self.dst))

# our graph
class Road_Graph:
    def __init__(self):
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

    def dump(self):
        print("Road Graph:\n=========================")
        print("Intersections:")
        for intersection in self.intersections.values():
            print(intersection)
        print("\nRoad_Segments:")
        for road_seg in self.road_segments.values():
            print(road_seg)

    def fdump(self):
        f = open("road_graph_dump.txt", "w")

        f.write("Road Graph:\n=========================")
        f.write("\nIntersections:")
        for intersection in self.intersections.values():
            f.write(str(intersection))
            f.write("\n")
        f.write("\nRoad_Segments:")
        for road_seg in self.road_segments.values():
            f.write(str(road_seg))
            f.write("\n")

        f.close