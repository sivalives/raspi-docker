# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api.py ./

# Expose port for the Flask app
EXPOSE 5000

# Run the Flask app
CMD ["python", "api.py"]

