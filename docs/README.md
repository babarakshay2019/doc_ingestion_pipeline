#  Document Ingestion Pipeline

A **modular**, **scalable**, and **event-driven** system built in **Python** using **FastAPI**, **Docker**, and **Google Cloud Pub/Sub** to ingest and extract structured text from documents and URLs. Designed for downstream use cases like **RAG**, **semantic search**, and **LLM pre-processing**.

---

##  Architecture Overview

```text
[ Ingestion API ] ──> [ Pub/Sub Topic ] ──> [ Extractor Service ] ──> [ Chunker Service ]
        │                        │                          │
        ▼                        ▼                          ▼
  File / URL Input        Smart Parsing         Text Chunking → GCS
```

---

## Project Structure

```text
doc_ingestion_pipeline/
│
├── docs/                        # Documentation
│   ├── PARSING_STRATEGY.md     # Parsing tools and cost/accuracy discussion
│   └── README.md               # This file
│
├── services/
│   ├── ingestion_api/          # FastAPI-based ingestion service
│   │   ├── api.py              # API endpoints
│   │   ├── main.py             # Service entrypoint
│   │   ├── pubsub_client.py    # Publishes to Pub/Sub
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── extractor/              # Document/URL text extraction service
│   │   ├── main.py
│   │   ├── extractor.py
│   │   ├── utils/
│   │   │   ├── ocr.py
│   │   │   ├── pdf_extractors.py
│   │   │   └── text_extractors.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── chunker/                # Chunking extracted text
│       ├── main.py
│       ├── chunking.py
│       ├── pubsub_handler.py
│       ├── Dockerfile
│       └── requirements.txt
│
├── shared/                     # Common utilities
│   ├── pubsub/
│   └── storage/
│       ├── file_utils.py
│       ├── gcs_client.py
│
├── terraform/                  # (Optional) Infra-as-code
│
├── .env                        # Environment configuration
├── docker-compose.yml          # Docker multi-service config
├── config.py                   # Centralized config values
└── pyproject.toml              # Linting/formatting dependencies
```

---

##  Features

- Ingest documents via **API** or **URL**
- Extract content from **PDF**, **DOCX**, **HTML**, and scanned files (via **OCR**)
- Use of **Pub/Sub** for service decoupling and scalability
- Multi-tenant metadata support
- Smart chunking with configurable size/overlap
- GCS integration for persistent storage
- Built for **RAG pipelines**, **LLM prep**, **search indexing**

---

##  Configuration

Configurations are managed via `.env` and `config.py`.

| Variable                     | Description                                     | Default                                  |
|-----------------------------|-------------------------------------------------|------------------------------------------|
| `CHUNK_SIZE`                | Number of characters per text chunk            | 1000                                     |
| `CHUNK_OVERLAP`             | Characters overlapped between chunks           | 200                                      |
| `MAX_RETRIES`               | Max retry attempts for Pub/Sub processing      | 3                                        |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to GCP service account JSON     | ingestion-pipeline-460412-*.json         |
| `GCP_PROJECT`               | Google Cloud project ID                         | ingestion-pipeline-460412                |
| `GCS_BUCKET`                | GCS bucket for output storage                   | ingestion-pipeline-bucket                |
| `PUBSUB_TOPIC`              | Pub/Sub topic for ingestion requests           | ingestion-request                         |
| `SUBSCRIPTION_NAME`         | Subscription for extractor service             | extractor-sub                             |
| `PUBSUB_EXTRACTION_TOPIC`   | Pub/Sub topic for extracted output             | extraction-topic                          |
| `PUBSUB_EMBEDDING_TOPIC`    | (Optional) Topic for embedding handoff         | embedding-topic                           |
| `CHUNKER_SUBSCRIPTION`      | Subscription for chunker service               | chunker-sub                               |

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/babarakshay2019/doc_ingestion_pipeline.git
cd doc_ingestion_pipeline
```

### 2. Configure Environment

Update `.env` with:

```env
GCS_BUCKET=your-bucket-name
PUBSUB_TOPIC=ingestion-request
SUBSCRIPTION_NAME=extractor-sub
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
OPENAI_API_KEY=your-api-key-if-needed
```

### 3. Authenticate with Google Cloud

```bash
gcloud auth application-default login
```

Or use a service account:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
```

---

## Run with Docker Compose

```bash
docker-compose up --build
```

Services started:

- `ingestion_api`: Accepts files/URLs and sends to Pub/Sub
- `extractor`: Subscribes to Pub/Sub, extracts text, uploads to GCS
- `chunker`: Chunks extracted text and republishes or stores

---

## API Endpoints

Visit Swagger UI at: [http://localhost:8000/docs](http://localhost:8000/docs)

### Upload File

```bash
curl -X POST http://localhost:8000/api/upload   -F "tenant_id=tenant123"   -F "file=@/path/to/document.pdf"
```

### Submit URL

```bash
curl -X POST http://localhost:8000/api/url   -H "Content-Type: application/x-www-form-urlencoded"   -d "tenant_id=tenant123&url=https://example.com"
```

---

## Parsing Strategy

We evaluate quality and cost trade-offs between tools like:

- `PyMuPDF`, `pdfplumber`, `Tesseract`, `Playwright`, `unstructured`
- Alternatives: AWS Textract, GROBID

Refer to [`docs/PARSING_STRATEGY.md`](docs/PARSING_STRATEGY.md) for full details.

---

## Development & Testing

Rebuild everything:

```bash
docker-compose down
docker-compose up --build
```

Format and lint:

```bash
ruff check .
```

---

## Tech Stack

- **Python 3.10+**
- **FastAPI**
- **Docker & Docker Compose**
- **Google Cloud Pub/Sub**
- **Google Cloud Storage**
- **PyMuPDF**, **pdfplumber**, **Tesseract**, **Playwright**

---