# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy all contents from the current directory to /app in the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to the outside world
EXPOSE 5000

# Script to generate SSL certificates
#COPY generate_cert.sh /app/generate_cert.sh
#RUN chmod +x /app/generate_cert.sh

# Run Gunicorn with SSL configuration
#CMD ["/bin/bash", "-c", "/app/generate_cert.sh && gunicorn --workers=4 --bind 0.0.0.0:5000 --certfile /app/certs/cert.pem --keyfile /app/certs/key.pem app:app"]
CMD ["python","app.py"]
