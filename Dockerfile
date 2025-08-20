FROM python:3.11-slim

WORKDIR /app

# Install Node.js (v20.x) and required libs
RUN apt-get update && \
    apt-get install -y \
        git \
        curl \
        build-essential \
        ffmpeg \
        libopus-dev \
        python3-dev \
        pkg-config \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip before installing
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot source code
COPY . .

# Set environment variable for port (optional)
ENV PORT=8080

# Run the bot when container starts
CMD ["python", "main.py"]
