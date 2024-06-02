echo "stopping all running containers"
docker stop $(docker ps | awk '{print $1}' | grep -v "CONTAINER")
docker system prune -f -a

