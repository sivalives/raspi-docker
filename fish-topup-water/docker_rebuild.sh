#!/bin/bash

#Stop container
docker stop fish-topup-water

#Delete container if any 
docker rm $(docker ps -a| grep fish-topup-water| cut -d " " -f1 )

#Delete image
docker image rm fish-topup-water

#Build image : 
docker build -t fish-topup-water .

#Run and create container
docker run --privileged -d --restart unless-stopped --name fish-topup-water fish-topup-water 

#Login to Docker Container : 
#docker exec -it fish-topup-water bash

#To keep containers running even after restart/powershutdown of Raspi
#docker update --restart unless-stopped $(docker ps -q)
