#  Document Ingestion Pipeline

This project implements a scalable, modular document ingestion pipeline using **Python**, **FastAPI**, **Google Cloud Pub/Sub**, and **Docker**. It extracts text from various file types and URLs, prepares content for downstream processing (e.g. RAG), and stores it in cloud storage and vector databases.

---

##  Project Structure

```
doc_ingestion_pipeline/
│
├── services/
│   ├── ingestion_api/         # FastAPI service for ingesting files and URLs
│   │   ├── main.py
│   │   ├── api.py
│   │   ├── utils.py
│   │   ├── pubsub_client.py
│   │   └── Dockerfile
│   │
│   ├── extractor/             # Extractor service to process documents and URLs
│   │   ├── main.py
│   │   ├── extractor.py
│   │   └── Dockerfile
│
├── shared/
│   ├── pubsub/                # Shared Pub/Sub utilities
│   │   ├── publisher.py
│   │   └── subscriber.py
│   │
│   ├── storage/               # Shared GCS and file handling
│   │   ├── gcs_client.py
│   │   └── file_utils.py
│
├── .env                       # Environment variables
├── docker-compose.yml        # Multi-service setup
└── README.md
```

---

##  Features

* Ingest documents via **API** or **URL**
* Extract text from PDF, DOCX, XLSX, and HTML
* Optional **OCR** for scanned files
* Uses **Pub/Sub** for event-driven microservices
* Multi-tenant support with metadata
* Ready for downstream **RAG embedding**

---

##  Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/babarakshay2019/doc_ingestion_pipeline.git
cd doc_ingestion_pipeline
```

### 2. Create `.env` file

```env
# .env
GCS_BUCKET=your-bucket-name
PUBSUB_TOPIC=ingestion-request
SUBSCRIPTION_NAME=extractor-sub
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
OPENAI_API_KEY=your-api-key-if-needed
```

### 3. Authenticate with Google Cloud

Make sure your local environment or container has access to GCP:

```bash
gcloud auth application-default login
```

Or mount a service account key in Docker (`GOOGLE_APPLICATION_CREDENTIALS`).

---

##  Run with Docker Compose

Start both services:

```bash
docker-compose up --build
```

This will spin up:

* `ingestion_api`: Listens for file/URL ingestion requests (available at [http://localhost:8000](http://localhost:8000))
* `extractor`: Subscribes to Pub/Sub and processes data

---

##  API Docs

After running the ingestion API, visit:

```
http://localhost:8000/docs
```

This opens the FastAPI Swagger UI to test `/upload` and `/url` endpoints interactively.

---

## Example API Calls

### Upload File

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "tenant_id=tenant123" \
  -F "file=@/path/to/your/document.pdf"
```

### Submit URL

```bash
curl -X POST http://localhost:8000/api/url \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "tenant_id=tenant123&url=https://example.com"
```

---

## Tech Stack

* **Python**
* **FastAPI**
* **Google Cloud Pub/Sub**
* **Google Cloud Storage**
* **Docker / Docker Compose**

---

##  Development

### Rebuild and restart services

```bash
docker-compose down
docker-compose up --build
```



---

## To-Do / Next Steps

* Add support for DOCX/XLSX
* Integrate OCR using GCP Vision API
* Add tests (unit & integration)
* Add CI/CD pipeline (e.g., GitHub Actions)
* Add Terraform scripts for infra provisioning

---