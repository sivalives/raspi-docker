#!/bin/bash

#Create volume for storing the output of IPTV to be used with another container for splunk UF
#docker volume create iptv-volume

#Stop container
docker stop docker-iptv

#Delete container if any 
docker rm $(docker ps -a| grep docker-iptv| cut -d " " -f1 )

#Delete image
docker image rm docker-iptv

#Build image : 
docker build -t docker-iptv .

#Run and create container
#docker run -d --restart unless-stopped --name docker-iptv docker-iptv
docker run -d --restart unless-stopped -v iptv-volume:/iptv-volume --name docker-iptv docker-iptv

#Login to Docker Container : 
#docker exec -it docker-iptv bash

#To keep containers running even after restart/powershutdown of Raspi
#docker update --restart unless-stopped $(docker ps -q)
