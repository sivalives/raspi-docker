#!/bin/bash

SSH_DIR="$HOME/.ssh"
GIT_KEY="$SSH_DIR/raspi_git"
PUB_GIT_KEY="${GIT_KEY}.pub"

echo "setting up ssh keys - update in git!!!"
mkdir -p $SSH_DIR
if [ ! -f $GIT_KEY ]; then
ssh-keygen -o -t rsa -C "sivalives@gmail.com" -f $GIT_KEY  -q -N ""
chmod 400 $GIT_KEY $PUB_GIT_KEY
else
echo "key exists"
fi

echo "Setting up config for git seamless"
git config --global user.email sivalives@gmail.com
git config --global user.name Siva
git remote set-url origin git@github.com:sivalives/raspi-docker.git

cat > $SSH_DIR/config <<EOF
Host github.com
        User git
        IdentitiesOnly yes
        IdentityFile $GIT_KEY
EOF

echo "Update this key to GIT "
cat $PUB_GIT_KEY



echo "installing Docker"
curl -fsSL https://get.docker.com | sh
echo "setting up ${USER} to have access to run docker"
sudo usermod -aG docker ${USER}
echo "Setting up docker-compose"
sudo apt -y install docker-compose
echo "enable boot start"
sudo systemctl enable docker

echo "installing telnet"
sudo apt -y install telnet

echo "Setting up ansible"
sudo apt install -y ansible

#Setup samba prerequisites!
bash ./samba/setup_samba_docker_volume.sh

