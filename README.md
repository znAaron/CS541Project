# CS541Project

Embedded Map Graph Database for time dependant queries

# How to setup the environment

## 1. setup the mysql and redis database

1a. install [docker](https://docs.docker.com/engine/install/)

1b. configure the environment variables to the desired value
```
export OSM_DB_HOST=localhost
export OSM_DB_PORT=3306
export OSM_DB_PWD=YOUR_PASSWORD
export OSM_REDIS_PORT=6379
export OSM_REDIS_PWD=YOUR_PASSWORD
export GMAP_APIKEY=API_KEY
```

1c. start the database using start-osm-mysql.sh

```
./databases/start-osm-databases.sh
```
## 2. populate the data

2a. install the required python packages using
```
pip install -r requirements.txt
```

2b. configure the configuration in config.ini

2c. modify the driver.py to use the dataset you want (no need to modify if using the small sample data)

2d. run the driver and you can find the output and logs under the output directory
```
python driver.py
```

## Suported commands

### Shortest Path Query

path sourceId destinationId visualizeFile(optional)

```
>path 5030761221 37997160 path1
```

### Range Query

range type latitude longitude range(m)

```
>range food 40.4274555 -86.9169385 500
```

### K Nearest Query

nearest type latitude longitude number

```
>nearest food 40.4274555 -86.9169385 3
```

### Exit

exit the database

```
>exit
```