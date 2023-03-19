# find the shortest path using A* algorithm
import logging
from queue import PriorityQueue
from src.graph.road_graph import *

def a_star_search(graph, src, dst):
    if src not in graph.intersections.keys() or \
        dst not in graph.intersections.keys():
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
        
        for next in graph.intersections.get(current).neighbours:
            new_cost = cost_so_far[current] + graph.delay(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + graph.harv_distance(next, dst)
                frontier.put(next, priority)
                came_from[next] = current
    
    cost = cost_so_far.get(dst)
    route = []
    curr = dst
    while curr is not None:
        route.append(curr)
        curr = came_from.get(curr)
    route.reverse()
    print(route)

    return route, cost