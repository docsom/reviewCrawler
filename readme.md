Please execute for_docker.py in main location -> ......./0914_shopping_crawler

for dockerfile

python3 /home/crawler/review_crawler/kurly/for_docker.py


attach to docker container(Windows Powershell)

docker exec -it <<container ID>> /bin/bash

docker exec -it d4a9e110404545be64b05ed87496fcad94441f0693d50f92f15395e9ad5e414c /bin/bash


detach to docker container

ctrl p q


to move docker's file to local

docker cp ((Container Name)):((Docker's location)) ((local's location))

docker cp Kurly_Crawler:/home/crawler/review_crawler/data/kurly/911006/reviews .