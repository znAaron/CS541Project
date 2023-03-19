# visualize the graph
import logging
import gmplot
import os

class Visualizer:
    def __init__(self, graph):
        self.logger = logging.getLogger(__name__)
        self.apikey = os.environ.get('GMAP_APIKEY')
        self.graph = graph

    def display_route(self, route, name):
        self.logger.info("start visualizing route")
        locations = self.graph.route_to_location(route)
        focus_point = self.graph.center_point(locations)
        gmap = gmplot.GoogleMapPlotter(focus_point[0], focus_point[1], 14, apikey=self.apikey)
        
        # draw the source and destination
        gmap.marker(locations[0][0], locations[0][1], color='green', title='Starting Point')
        gmap.marker(locations[-1][0], locations[-1][1], color='red', title='Destination')

        # draw waypoints
        waypoints_lats, waypoints_lngs = zip(*locations[1:-1])
        gmap.scatter(waypoints_lats, waypoints_lngs, color='blue', size=6, fa=1, ew=0, marker=False)

        # draw path
        path = zip(*locations)
        gmap.plot(*path, edge_width=6, color='#00bfff')

        output_path = os.path.dirname("./output/")
        output_name = name + ".html"
        output_file = os.path.join(output_path, output_name)
        gmap.draw(output_file)
        self.logger.info("finish visualizing route")