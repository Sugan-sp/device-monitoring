# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY monitor.py devices.json ./

# Run the monitor
CMD ["python", "monitor.py"]
