FROM python:latest
COPY lifx.py /bin/lifx-automation/lifx.py
COPY power_failure_lifx_shutoff.py /bin/lifx-automation/power_failure_lifx_shutoff.py
COPY dropbox_utils_v2.py /bin/lifx-automation/dropbox_utils_v2.py
RUN chmod -R +x /bin/lifx-automation
RUN apt-get update -y
RUN apt-get -y install vim python3-pip 
RUN pip install dropbox
CMD python3 /bin/lifx-automation/power_failure_lifx_shutoff.py
