import logging
import shapely

class Query_Processor:
    def __init__(self, graph):
        self.logger = logging.getLogger(__name__)
        self.graph = graph
        
    def accept_query(self):
        while True:
            query = input(">")
            commands = query.split()
            valid_query = False

            if len(commands) == 0:
                valid_query = False
            elif commands[0] == "path":
                valid_query = self.path_query(commands[1:])
            elif commands[0] == "range":
                valid_query = self.range_query(commands[1:])
            elif commands[0] == "nearest":
                valid_query = self.nearst_query(commands[1:])
            elif commands[0] == "exit":
                return
            
            if not valid_query:
                print("error parsing query")

    def path_query(self, commands):
        commands_num = len(commands)
        if commands_num < 2:
            return False
        src, dst = int(commands[0]), int(commands[1])
        self.logger.info(f"start processing path query form {src} to {dst}")

        route, cost = self.graph.pathfinder.find_route(src, dst)
        if route is None:
            return False
        print(f"{cost} seconds")
        print(route)

        if commands_num > 2:
            file_name = commands[2]
            self.graph.visualizer.display_route(route, file_name)

        self.logger.info(f"finish processing path query form {src} to {dst}")
        return True
    
    def range_query(self, commands):
        commands_num = len(commands)
        if commands_num < 4:
            return False
        location_type = commands[0]
        lat, lon = float(commands[1]), float(commands[2])
        range = int(commands[3])
        self.logger.info(f"start processing range query of type {location_type} form {lat}, {lon} with radious of {range}")

        lon_lat = self.valid_lonlat(lon, lat)
        if lon_lat is None:
            self.logger.error(f"{lon}, {lat} is not in WGS84 bounds")
            return False
        else:
            lon, lat = lon_lat

        result = self.graph.rangefinder.find_range(location_type, lat, lon, range)
        print(result)

        self.logger.info(f"finish processing range query of type {location_type} form {lat}, {lon} with radious of {range}")
        return True

    def nearst_query(self, commands):
        commands_num = len(commands)
        if commands_num < 4:
            return False
        location_type = commands[0]
        lat, lon = float(commands[1]), float(commands[2])
        count = int(commands[3])
        self.logger.info(f"start processing nearest query of type {location_type} form {lat}, {lon} with radious of {range}")

        lon_lat = self.valid_lonlat(lon, lat)
        if lon_lat is None:
            self.logger.error(f"{lon}, {lat} is not in WGS84 bounds")
            return False
        else:
            lon, lat = lon_lat

        result = self.graph.rangefinder.find_near(location_type, lat, lon, count)
        print(result)

        self.logger.info(f"finish processing nearest query of type {location_type} form {lat}, {lon} with radious of {range}")
        return True
    
    def valid_lonlat(self, lon, lat):
        """
        This validates a lat and lon point can be located
        in the bounds of the WGS84 CRS, after wrapping the
        longitude value within [-180, 180)

        :param lon: a longitude value
        :param lat: a latitude value
        :return: (lon, lat) if valid, None otherwise
        """
        lon %= 360
        if lon >= 180:
            lon -= 360
        lon_lat_point = shapely.geometry.Point(lon, lat)
        lon_lat_bounds = shapely.geometry.Polygon.from_bounds(
            xmin=-180.0, ymin=-90.0, xmax=180.0, ymax=90.0
        )
        if lon_lat_bounds.intersects(lon_lat_point):
            return lon, lat

