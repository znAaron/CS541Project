# abstract the database interface
import logging
import os
import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'osm-db'

TABLES = {}
TABLES['nodes'] = (
    "CREATE TABLE `nodes` ("
    "  `id` BIGINT NOT NULL,"
    "  `lat` float NOT NULL,"
    "  `lon` float NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

class OSM_Database:
  def __init__(self):
    self.logger = logging.getLogger(__name__)

    # connect to mysql database
    dbhost = os.environ.get('OSM_DB_HOST')
    dbport = os.environ.get('OSM_DB_PORT')
    if dbhost is None or dbport is None or os.environ.get('OSM_DB_PWD') is None:
      self.logger.error(f"failed to load environment varibles please set them before use")
    
    self.logger.info(f"connecting mysql database @{dbhost}:{dbport}")
    self.osm_db = mysql.connector.connect(
      host = dbhost,
      port = dbport,
      user = "osm-user",
      password = os.environ.get('OSM_DB_PWD'),
      database="osm-db"
    )
    self.create_tables()

    self.node_cache = []

  def create_tables(self):
    cursor = self.osm_db.cursor()
    for table_name in TABLES:
      table_description = TABLES[table_name]
      try:
          self.logger.info(f"Creating table {table_name} ")
          cursor.execute(table_description)
      except mysql.connector.Error as err:
          if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
              self.logger.warn(f"skip creating table {table_name} because already exists.")
          else:
              self.logger.exception(err.msg)
      else:
          self.logger.info(f"table {table_name} created")
    cursor.close()

  def insert_node(self, id, lat, lon):
    self.node_cache.append((id, lat, lon))
    if (len(self.node_cache) > 65536):
      self.flush_node()

  def flush_node(self):
    cursor = self.osm_db.cursor()
    query = "INSERT INTO nodes (id, lat, lon) VALUES (%s, %s, %s)"
    cursor.executemany(query, self.node_cache)
    self.osm_db.commit()
    self.node_cache = []
    cursor.close()

  def get_node(self, id):
    cursor = self.osm_db.cursor()
    query = "SELECT * FROM nodes WHERE id = %s"
    cursor.execute(query, id)
    row = cursor.fetchone()
    cursor.close()

    if row is None:
      self.logger.error(f"fetch node failed with id {id} ")
      return None
    return Node(row.id, row.lat, row.lon)

  def close(self):
    self.osm_db.close()