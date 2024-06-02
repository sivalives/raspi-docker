#!/bin/bash

#Stop container
docker stop docker-lifx-automation

#Delete container if any 
docker rm $(docker ps -a| grep docker-lifx-automation| cut -d " " -f1 )

#Delete image
docker image rm docker-lifx-automation

#Build image : 
docker build -t docker-lifx-automation .

#Run and create container
docker run -d --restart unless-stopped --name docker-lifx-automation docker-lifx-automation

#Login to Docker Container : 
#docker exec -it docker-lifx-automation bash

#To keep containers running even after restart/powershutdown of Raspi
#docker update --restart unless-stopped $(docker ps -q)
