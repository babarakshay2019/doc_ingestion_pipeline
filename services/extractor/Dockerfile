FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    libxml2-dev \
    libxslt-dev \
    tesseract-ocr \
    libsm6 libxext6 libxrender-dev \
    libmagic1 \
    swig \
    libpulse-dev \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

COPY services/extractor /app
COPY shared /app/shared

RUN pip install --upgrade pip==24.0
RUN pip install -r requirements.txt
ENV PYTHONPATH="${PYTHONPATH}:/app:/app/shared"
CMD ["python", "main.py"]
