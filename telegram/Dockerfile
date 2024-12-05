# Pass telegram API Token while running container!!!
FROM python:latest

# Copy your scripts into the container
COPY telegram-bot.py /bin/telegram/telegram-bot.py
COPY telegram-channel-poller.py /bin/telegram/telegram-channel-poller.py
COPY dropbox_utils_v2.py /bin/telegram/dropbox_utils_v2.py
COPY lifx.py /bin/telegram/lifx.py
COPY dropbox_setup.py /bin/telegram/dropbox_setup.py
COPY log2rabbitmq.py /bin/telegram/log2rabbitmq.py
COPY requirements.txt /bin/telegram/requirements.txt

# Ensure the necessary permissions
RUN chmod -R +x /bin/telegram

# Update the container's package list and install required packages
RUN apt-get update -y

# Install Docker client (for interacting with Docker host)
RUN apt-get -y install apt-transport-https ca-certificates curl software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
RUN apt-get update -y && apt-get -y install docker.io

# Install other dependencies from requirements.txt
RUN apt-get -y install vim python3-pip
RUN pip install --requirement /bin/telegram/requirements.txt

# Set the default command to run the Telegram bot script
CMD python3 /bin/telegram/telegram-bot.py
