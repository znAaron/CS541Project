# load configuration
from configparser import ConfigParser

# read configuration
def config_init():
    config_object = ConfigParser()
    config_object.read("config.ini")
    global server_config
    server_config = config_object["SERVER"]
    global query_config
    query_config = config_object["QUERY"]