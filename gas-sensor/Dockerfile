#Python script to check LPG/GAS leak 
FROM python:latest
COPY requirements.txt /bin/gas/requirements.txt
COPY gas_sensor.py /bin/gas/gas_sensor.py
COPY dropbox_utils_v2.py /bin/gas/dropbox_utils_v2.py
RUN apt-get update -y && \
    apt-get -y install vim python3-pip
RUN pip install --requirement /bin/gas/requirements.txt
RUN chmod +x /bin/gas/gas_sensor.py
WORKDIR /bin/gas
CMD ["python", "gas_sensor.py"]
