#Pass telegram API Token while running container!!!
FROM python:latest
COPY telegram-bot.py  /bin/telegram/telegram-bot.py
COPY telegram-channel-poller.py /bin/telegram/telegram-channel-poller.py
COPY dropbox_utils_v2.py /bin/telegram/dropbox_utils_v2.py
COPY lifx.py /bin/telegram/lifx.py
COPY log2rabbitmq.py /bin/telegram/log2rabbitmq.py
COPY requirements.txt /bin/telegram/requirements.txt
RUN chmod -R +x /bin/telegram
RUN apt-get update -y
RUN apt-get -y install vim python3-pip 
RUN pip install --requirement /bin/telegram/requirements.txt
CMD python3 /bin/telegram/telegram-bot.py
