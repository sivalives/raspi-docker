FROM python:latest

# Set the working directory
WORKDIR /app

# Copy the Python scripts and other required files
COPY led_control.py /app/
COPY log2splunk.py /app/
COPY log2rabbitmq.py /app/
COPY requirements.txt /app/
COPY cronfile /etc/cron.d/fishlight-cron

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install cron and other utilities
RUN apt-get update && apt-get install -y cron vim && \
    chmod 0644 /etc/cron.d/fishlight-cron && \
    touch /var/log/cron.log && \
    chmod +x /etc/cron.d/fishlight-cron

# Ensure the cron job is recognized
RUN cat /etc/cron.d/fishlight-cron

# Start both cron and the Python script
CMD cron -f & python3 led_control.py

