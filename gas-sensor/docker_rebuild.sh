#!/bin/bash

#Stop container
docker stop gas-sensor

#Delete container if any 
docker rm $(docker ps -a| grep gas-sensor| cut -d " " -f1 )

#Delete image
docker image rm gas-sensor

#Build image : 
docker build -t gas-sensor .

#Run and create container
docker run --privileged -d --restart unless-stopped --name gas-sensor gas-sensor 

#Login to Docker Container : 
#docker exec -it gas-sensor bash

#To keep containers running even after restart/powershutdown of Raspi
#docker update --restart unless-stopped $(docker ps -q)
