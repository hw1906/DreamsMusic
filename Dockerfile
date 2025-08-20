FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && \
    apt-get install -y curl git ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js (v20.x) only if needed
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot source code
COPY . .

# Set environment variable for port
ENV PORT=8080

# Run the bot
CMD ["python", "main.py"]
