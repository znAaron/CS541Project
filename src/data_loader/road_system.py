# road system contains all the information we want for the map
from road_graph import *

road_types = {"motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", "residential"}
linkroad_types = {"motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link"}

class Road:
    def __init__(self, id, name, nodes, speedlimit):
        self.id = id
        self.name = name
        self.speedlimit = speedlimit

        self.nodes = []

        if isinstance(nodes[0], int):
            self.nodes = nodes
        else:
            for n in nodes:
                self.nodes.append(n.ref)
        self.src = self.nodes[0]
        self.dst = self.nodes[len(nodes) - 1]

    def __str__(self):
        return "{}({}), {}mph, [{} -> {}]".format(
            self.name, str(self.id), str(self.speedlimit), str(self.src), str(self.dst))

class Road_System:
    def __init__(self):
        self.named_roads = {}
        self.link_roads = []
        self.junction_roads = []

        self.processed_roads = []

        self.way_points = set()
        self.intersections = set()

    def add_linked_road(self, road):
        self.link_roads.append(road)

    def add_junction_road(self, road):
        self.junction_roads.append(road)

    def add_named_road(self, road):
        if road.name in self.named_roads:
            self.named_roads[road.name].append(road)
        else:
            self.named_roads[road.name] = [road]

    # todo: combine roads only with the same speed limit
    def combine_named_roads(self):
        self.processed_roads.extend(self.link_roads)
        self.processed_roads.extend(self.junction_roads)
        for road_list in self.named_roads.values():
            road_num = len(road_list)
            
            combined_list = []
            visited = [False] * road_num
            for i in range(road_num):
                if visited[i]:
                    continue
                visited[i] = True
                curr_road = road_list[i]

                j = i + 1
                while j < road_num:
                    if visited[j] or not self.can_combine_roads(curr_road, road_list[j]):
                        j += 1
                    else:
                        visited[j] = True
                        curr_road = self.combine_roads(curr_road, road_list[j])
                        j = i + 1
                
                combined_list.append(curr_road)
            self.processed_roads.extend(combined_list)

    def can_combine_roads(self, r1, r2):
        return r1.src == r2.src \
            or r1.dst == r2.dst \
            or r1.src == r2.dst \
            or r1.dst  == r2.src

    def combine_roads(self, r1, r2):
        node_list = []
        if r1.src == r2.src:
            node_list = r1.nodes[::-1] + r2.nodes[1:]
        elif r1.dst == r2.dst:
            node_list = r1.nodes[:-1] + r2.nodes[::-1]
        elif r1.src == r2.dst:
            node_list = r2.nodes + r1.nodes[1:]
        elif r1.dst  == r2.src:
            node_list = r1.nodes + r2.nodes[1:]
        
        combined_road = Road(r1.id, r1.name, node_list, r1.speedlimit)
        return combined_road

    def find_interesection(self):
        for road in self.processed_roads:
            self.intersections.add(road.src)
            self.intersections.add(road.dst)

            for i, node in enumerate(road.nodes[1:-1]):
                if node in self.intersections:
                    continue
                if node in self.way_points:
                    self.way_points.remove(node)
                    self.intersections.add(node)
                else:
                    self.way_points.add(node)
        print("way point count: {}, intersection count {}"
            .format(len(self.way_points), len(self.intersections)))

    def load_roads(self, graph):
        for road in self.processed_roads:
            prev = road.nodes[0]
            way_points = []
            for i, node in enumerate(road.nodes[1:]):
                if node in self.intersections:
                    road_seg = Road_Segment(road.id, road.name, prev, \
                        node, road.speedlimit, way_points)
                    graph.add_road_segment(road_seg)
                    prev = node
                    way_points = []
                else:
                    way_points.append(node)
    
    def dump(self):
        for road in self.processed_roads:
            print(road)

