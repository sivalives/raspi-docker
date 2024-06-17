#!/bin/bash

#Stop container
docker stop flask-dropbox

#Delete container if any 
docker rm $(docker ps -a| grep flask-dropbox| cut -d " " -f1 )

#Delete image
docker image rm flask-dropbox

#Build image : 
docker build -t flask-dropbox .

#Run and create container [ use mount to save the token to raspi local for reuse or no re-registration ]
docker run --privileged -d --restart unless-stopped -p 5000:5000 --mount source=token_data,target=/app/token_data --name flask-dropbox flask-dropbox  

#Login to Docker Container : 
#docker exec -it flask-dropbox bash

#To keep containers running even after restart/powershutdown of Raspi
#docker update --restart unless-stopped $(docker ps -q)

#Create volume for storing the token used for dropbox API
docker volume create token_data
