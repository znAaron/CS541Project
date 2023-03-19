# visualize the graph
import logging
import gmplot
import os

class Visualizer:
    def __init__(self, graph):
        self.logger = logging.getLogger(__name__)
        self.apikey = os.environ.get('GMAP_APIKEY')
        self.graph = graph

    def display_route(self, route):
        self.logger.info("start visualizing route")
        locations = self.graph.route_to_location(route)
        focus_point = self.graph.center_point(locations)
        gmap = gmplot.GoogleMapPlotter(focus_point[0], focus_point[1], 14, apikey=self.apikey)
        gmap.directions(
            locations[0],
            locations[-1],
            waypoints=locations[1:-1]
        )
        gmap.draw('./output/map.html')
        self.logger.info("finish visualizing route")