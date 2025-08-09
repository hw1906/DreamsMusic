FROM python:3.11-slim

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
