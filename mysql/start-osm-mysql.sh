# Not necessary the best practice to setup the password
# change before production
rm -rf osm-mysql-env.yaml; \
envsubst < "osm-mysql.yaml" > "osm-mysql-env.yaml"; \
docker-compose -f osm-mysql-env.yaml up -d; \
rm -rf osm-mysql-env.yaml