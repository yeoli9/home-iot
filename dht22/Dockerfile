# Use a slim Python base image
FROM python:3.13-slim

# Install system dependencies (pigpio daemon)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      libgpiod2 \
      python3-libgpiod \
      python3-rpi.gpio \
      python3-dev \
      libffi-dev \
      libatlas-base-dev \
      gcc \
      build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install RPi.GPIO

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and JSON payloads
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start pigpio daemon and Uvicorn server
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

