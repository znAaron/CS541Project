# find the shortest path using A* algorithm
# Reference: https://www.redblobgames.com/pathfinding/a-star/implementation.html
import logging
from queue import PriorityQueue
from src.graph.road_graph import *

class Pathfinder:
    def __init__(self, graph):
        self.logger = logging.getLogger(__name__)
        self.graph = graph

    # shortest
    def a_star_search(self, src, dst):
        self.logger.info(f"start finding path from {src} to {dst} using A* algorithm")
        if src not in self.graph.intersections.keys() or \
            dst not in self.graph.intersections.keys():
            self.logger.error(f"can not finding path from {src} to {dst} because the intersection id is not recognized")
            return None

        frontier = PriorityQueue()
        frontier.put(src, 0)

        came_from = {}
        cost_so_far = {}
        came_from[src] = None
        cost_so_far[src] = 0
        
        while not frontier.empty():
            current = frontier.get()
            
            if current == dst:
                break
            
            for next in self.graph.intersections.get(current).neighbours:
                new_cost = cost_so_far[current] + self.graph.delay(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.graph.harv_distance(next, dst)
                    frontier.put(next, priority)
                    came_from[next] = current
        
        cost = cost_so_far.get(dst)
        route = reconstruct_path(came_from, dst)
        self.logger.info(f"finish finding path from {src} to {dst} using A* algorithm")

        return route, cost

    def dijkstra_search(self, src, dst):
        self.logger.info(f"start finding path from {src} to {dst} using dijkstra algorithm")
        if src not in self.graph.intersections.keys() or \
            dst not in self.graph.intersections.keys():
            self.logger.error(f"can not finding path from {src} to {dst} because the intersection id is not recognized")
            return None

        frontier = PriorityQueue()
        frontier.put(src, 0)

        came_from = {}
        cost_so_far = {}
        came_from[src] = None
        cost_so_far[src] = 0
        
        while not frontier.empty():
            current = frontier.get()
            
            if current == dst:
                break
            
            for next in self.graph.intersections.get(current).neighbours:
                new_cost = cost_so_far[current] + self.graph.delay(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    frontier.put(next, priority)
                    came_from[next] = current

        cost = cost_so_far.get(dst)
        route = reconstruct_path(came_from, dst)

        self.logger.info(f"finish finding path from {src} to {dst} using dijkstra algorithm")
        return route, cost

# utilities
def reconstruct_path(came_from, dst):
    path = []
    curr = dst
    while curr is not None:
        path.append(curr)
        curr = came_from.get(curr)
    path.reverse()

    return path