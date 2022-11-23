#!/bin/bash
echo 'removing docker services...'
docker service ls | awk {' print $1 '} | tail -n+2 > tmp.txt; for line in $(cat tmp.txt);\
do docker service rm $line; \
done; rm tmp.txt; \

echo 'removing docker containers...'; \
docker ps | awk {' print $1 '} | tail -n+2 > tmp.txt; for line in $(cat tmp.txt);\
do docker kill $line; \
docker update --restart=no $line; \
done; rm tmp.txt; \
echo 'pruning volumes, networks and whatever'; \
docker system prune  -a -f; \
docker volume prune -f; \
echo "done";