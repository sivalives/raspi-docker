#/bin/bash
sudo docker volume create iptv-volume
sudo docker pull trnape/rpi-samba
if [ -z $1 ] || [ -z $2 ]; then
  echo "pass samba server username and password you want to use"
  exit
else
  docker stop docker-samba && docker rm -f docker-samba
  sudo docker run -d -p 127.0.0.1:445:445 -v /var/lib/docker/volumes/iptv-volume/_data:/share/data --name docker-samba trnape/rpi-samba -u "$1:$2" -s "pi-files:/share/data/:rw:pi"
fi 
sudo docker update --restart unless-stopped $(docker ps -q)
