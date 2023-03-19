# Not necessary the best practice to setup the password
# change before production
rm -rf osm-databases-env.yaml; \
envsubst < "osm-databases.yaml" > "osm-databases-env.yaml"; \
docker-compose -f osm-databases-env.yaml up -d; \
rm -rf osm-databases-env.yaml