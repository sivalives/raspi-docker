#Python script to topup water in tank
FROM python:latest
COPY requirements.txt /bin/fish-topup/requirements.txt
COPY fish-topup-water.py /bin/fish-topup/fish-topup-water.py
RUN apt-get update -y && \
    apt-get -y install vim python3-pip
RUN pip install --requirement /bin/fish-topup/requirements.txt
RUN chmod +x /bin/fish-topup/fish-topup-water.py
WORKDIR /bin/fish-topup
CMD ["python", "fish-topup-water.py"]
