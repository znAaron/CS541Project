import logging
import logging.config
import yaml
import time
import os
from src.data_loader.osm_parser import *

# define the data files
SAMPLE_FILE = "./data/osm-sm/west_lafayette.osm"
DATA_FILE = "./data/osm-lg/us-midwest-latest.osm.pbf"

if not os.path.exists("output/logs"):
   os.makedirs("output/logs")

# initialize the logger
def logmaker():
    log_path = os.path.dirname("./output/logs/")
    log_name = "graph_database-" + time.strftime("%Y%m%d-%H%M%S") + ".log"
    path = os.path.join(log_path, log_name)
    return logging.FileHandler(path)

with open('logger.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

# main function
def main():
    osm_data = SAMPLE_FILE
    logger.info(f"loading data from file: {osm_data}")

    osm_parser = OSM_Parser(osm_data)
    osm_parser.load_sample_data()

if __name__ == "__main__":
    main()