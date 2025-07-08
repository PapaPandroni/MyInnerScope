FROM python:3.11-slim

# Install core system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for library paths (if needed, though apt-get should handle this)
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:/usr/lib:/lib/x86_64-linux-gnu:/lib
ENV PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/share/pkgconfig

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port (Railway will use $PORT from your start command)
EXPOSE 8000

# Command to run the application (from Procfile)
CMD gunicorn --bind 0.0.0.0:$PORT 'app:create_app()' --workers 3