class Intersection:
    def __init__(self, id, lat, lon):
        self.id = id
        self.latitude = lat
        self.longitude = lon
        self.neighbours = []

    def add_neighbour(n):
        neighbours.append(n)

class Road_Segment:
    def __init__(self, src, dst, speed, shape):
        self.id = id
        self.src = src
        self.dst = dst
        self.length = 10
        self.delay = length/speed
        self.neighbours = []

class Road_Graph:
    def __init__(self):
        # id to intersection dictionary
        self.intersections = {}
        # src:dst to road_segment dictionary
        self.road_segments = {}
        
    def shortest_path_dijkstra:
        # To implement

    def shortest_path_astar:
        # To implement