#Python script to feed the fish daily - use stepper motor or servo motor 
#Check crontab file where input and output for python script is specified. Output directs to volume!
FROM python:latest
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /bin/fish/requirements.txt
COPY servo_motor_180.py /bin/fish/servo_motor_180.py
COPY dropbox_utils_v2.py /bin/fish/dropbox_utils_v2.py
ADD cronfile /etc/cron.d/fish-cron
RUN touch /var/log/cron.log
RUN chmod 0644 /etc/cron.d/fish-cron
RUN chmod -R +x /bin/fish
RUN apt-get update -y
RUN apt-get -y install cron vim python3-pip
RUN pip install --requirement /bin/fish/requirements.txt
CMD cron && tail -f /var/log/cron.log
