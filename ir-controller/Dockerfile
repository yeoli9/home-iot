# Use a slim Python base image
FROM python:3.11-slim

# Install system dependencies (pigpio daemon)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       pigpio-tools \
       python3-pigpio \
    && rm -rf /var/lib/apt/lists/*

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
CMD ["fastapi", "run", "app/app.py", "--port", "8000", "--reload"]

