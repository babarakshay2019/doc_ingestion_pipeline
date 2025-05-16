FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    libreoffice \
    libxml2-dev \
    libxslt-dev \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install textract beautifulsoup4 requests google-cloud-pubsub google-cloud-storage

CMD ["python", "main.py"]
