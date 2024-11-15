FROM python:3.9
WORKDIR /app

# Install required Python libraries
RUN pip install paho-mqtt flask

# Copy the publisher script and API logic
COPY api.py /app

# Run the API server
CMD ["python", "api.py"]

