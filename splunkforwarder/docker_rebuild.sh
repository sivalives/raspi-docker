#!/bin/bash

#Stop container
docker stop docker-splunkuf

#Delete container if any 
docker rm $(docker ps -a| grep docker-splunkuf| cut -d " " -f1 )

#Delete image
docker image rm docker-splunkuf

#Build image : 
docker build -t docker-splunkuf .

#Run and create container
#Use the volume populated by docker-iptv container
docker run -td --restart unless-stopped -v iptv-volume:/iptv-volume --name docker-splunkuf docker-splunkuf 

#Login to Docker Container : 
#docker exec -it docker-splunkuf bash

#To keep containers running even after restart/powershutdown of Raspi
#docker update --restart unless-stopped $(docker ps -q)

