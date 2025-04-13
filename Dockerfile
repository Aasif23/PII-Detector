FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Container startup
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app