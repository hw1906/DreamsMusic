FROM python:3.11-slim

WORKDIR /app

# Install Node.js (v20.x)
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot source code
COPY . .

# Set environment variable for port (optional)
ENV PORT=8080

# Run the bot when container starts
CMD ["python", "main.py"]FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot source code
COPY . .

# Set environment variable for port (optional)
ENV PORT=8080

# Run the bot when container starts
CMD ["python", "main.py"]
