#!/bin/bash

#Stop container
docker stop fish-lights

#Delete container if any 
docker rm $(docker ps -a| grep fish-lights| cut -d " " -f1 )

#Delete image
docker image rm fish-lights

#Build image : 
docker build -t fish-lights .

#Run and create container
docker run --privileged -d --restart unless-stopped --name fish-lights fish-lights --network  mynetwork

#Login to Docker Container : 
#docker exec -it fish-lights bash

#To keep containers running even after restart/powershutdown of Raspi
#docker update --restart unless-stopped $(docker ps -q)
