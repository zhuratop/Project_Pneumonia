# Use Python 3.11.9 slim image as base
FROM python:3.11.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    TZ=Europe/Moscow \
    DEBIAN_FRONTEND=noninteractive

# Update system and install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    tzdata \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

# Create and set working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p uploads models

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Update pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Clean up unnecessary files
RUN find /app -type d -name "__pycache__" -exec rm -r {} + \
    && find /app -type f -name "*.pyc" -delete \
    && find /app -type f -name "*.pyo" -delete \
    && find /app -type f -name "*.pyd" -delete \
    && rm -rf /app/.git* /app/.idea* /app/*.iml /app/venv* /app/.venv* \
    && rm -rf /app/notebook.ipynb /app/*.bat /app/*.sh

# Expose port
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py \
    FLASK_ENV=production

# Run the application in detached mode
CMD ["python", "-u", "app.py"]