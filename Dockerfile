FROM python:3.11-slim

# Update package list and install WeasyPrint dependencies
RUN apt-get update && apt-get install -y \
    python3-weasyprint \
    python3-pip \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for library paths
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:/usr/lib:/lib/x86_64-linux-gnu:/lib
ENV PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/share/pkgconfig

WORKDIR /app

# Copy requirements and install dependencies (make sure weasyprint is removed from requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port (Railway will use $PORT from your start command)
EXPOSE 8000