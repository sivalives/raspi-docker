FROM python:latest
WORKDIR /app
COPY led_control.py /app/
COPY log2splunk.py /app/
COPY log2rabbitmq.py /app/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python3", "led_control.py"]
# Default command (could be overridden by Docker or the user when running the container)
CMD ["off"]  # Default to turn off the LED

