#!/bin/bash

#Stop container
docker stop fish-feeder

#Delete container if any 
docker rm $(docker ps -a| grep fish-feeder| cut -d " " -f1 )

#Delete image
docker image rm fish-feeder

#Build image : 
docker build -t fish-feeder .

#Run and create container
docker run --privileged -d --restart unless-stopped --name fish-feeder fish-feeder

#Login to Docker Container : 
#docker exec -it fish-feeder bash

#To keep containers running even after restart/powershutdown of Raspi
#docker update --restart unless-stopped $(docker ps -q)
