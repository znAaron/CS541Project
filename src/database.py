from src.data_loader.osm_database import *
from src.data_loader.osm_redis import *

def database_init():
    global sql_database
    sql_database = OSM_Database()
    global redis_database
    redis_database = OSM_Redis()

def database_close():
    sql_database.close()