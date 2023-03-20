# CS541Project

Embedded Map Graph Database for time dependant queries

# How to setup the environment

## 1. setup the mysql database

1a. install [docker](https://docs.docker.com/engine/install/)

1b. configure the environment variable OSM_DB_HOST, OSM_DB_PORT, and OSM_DB_PWD to the desired value
```
export OSM_DB_HOST=localhost
export OSM_DB_PORT=3306
export OSM_DB_PWD=YOUR_PASSWORD
```

1c. start the database using start-osm-mysql.sh

```
./mysql/start-osm-mysql.sh
```
## 2. populate the data

2a. install the required python packages using
```
pip install -r requirements.txt
```

2b. modify the driver.py to use the dataset you want (no need to modify if using the small sample data)

2c. run the driver and you can find the output and logs under the output directory
```
python driver.py
```

## Suported query types

### Shortest Path Query

path sourceId destinationId visualizeFile(optional)

e.g.  path 5030761221 37997160 path1

### Range Query

range type latitude longitude range(m)

e.g.  range food 40.4274555 -86.9169385 500

### K Nearest Query

nearest type latitude longitude number

e.g.  nearest food 40.4274555 -86.9169385 3