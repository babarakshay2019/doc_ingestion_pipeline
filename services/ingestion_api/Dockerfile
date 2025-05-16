# services/ingestion_api/Dockerfile

FROM python:3.11-slim

# Set environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system deps
RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install fastapi uvicorn aiofiles google-cloud-storage google-cloud-pubsub python-multipart

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
