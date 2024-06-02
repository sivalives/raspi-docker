#Python script to validate m3u8 files and stores output in docker volume. 
#Docker volume can be accessed here /var/lib/docker/volumes/1087d7e4a3abaf13dae887d82188ea7ff5d92899c8bd3370126799fe052d4b37/_data/output-playlist.m3u which splunk can ingest
#Check crontab file where input and output for python script is specified. Output directs to volume!
FROM python:latest
COPY iptv-threaded-scanner.py /bin/iptv/iptv-threaded-scanner.py
COPY requirements.txt /bin/iptv/requirements.txt
COPY input-playlist.m3u /bin/iptv/input-playlist.m3u
COPY iptv-zee5-scanner.py /bin/iptv/iptv-zee5-scanner.py
COPY dropbox_utils_v2.py /bin/iptv/dropbox_utils_v2.py
ADD cronfile /etc/cron.d/iptv-cron
RUN touch /var/log/cron.log
RUN chmod 0644 /etc/cron.d/iptv-cron
RUN chmod -R +x /bin/iptv
RUN apt-get update -y
RUN apt-get -y install cron vim python3-pip 
RUN pip install --requirement /bin/iptv/requirements.txt
CMD cron && tail -f /var/log/cron.log
