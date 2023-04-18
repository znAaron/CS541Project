import logging
import logging.config
import yaml
import time
import os
from src.conf import *
from src.database import *
from src.data_loader.osm_parser import *
from src.query.query_processor import *

config_init()

# define the data files
SAMPLE_FILE = "./data/osm-sm/west_lafayette.osm"
DATA_FILE = "./data/osm-lg/us-midwest-latest.osm.pbf"

if not os.path.exists("output/logs"):
   os.makedirs("output/logs")

# initialize the logger
def logmaker():
    log_path = os.path.dirname("./output/logs/")
    log_name = "demo.log"
    path = os.path.join(log_path, log_name)
    return logging.FileHandler(path)

with open('logger.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger(__name__)

# main function
def main():
    database_init()

    osm_data = SAMPLE_FILE
    logger.info(f"loading data from file: {osm_data}")
    parser = OSM_Parser(osm_data)
    graph = parser.load_sample_data()

    processor = Query_Processor(graph)
    processor.accept_query()
    database_close()

if __name__ == "__main__":
    main()