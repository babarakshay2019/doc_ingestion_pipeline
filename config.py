# config.py
import os

from dotenv import load_dotenv

load_dotenv()

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS", "ingestion-pipeline-460412-a183aa8f40bb.json"
)
GCP_PROJECT = os.getenv("GCP_PROJECT", "ingestion-pipeline-460412")
GCS_BUCKET = os.getenv("GCS_BUCKET", "ingestion-pipeline-bucket")
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC", "ingestion-request")
SUBSCRIPTION_NAME = os.getenv("SUBSCRIPTION_NAME", "extractor-sub")
PUBSUB_EXTRACTION_TOPIC = os.getenv("PUBSUB_EXTRACTION_TOPIC", "extraction-topic")
PUBSUB_EMBEDDING_TOPIC = os.getenv("PUBSUB_EMBEDDING_TOPIC", "embedding-topic")
CHUNKER_SUBSCRIPTION = os.getenv("CHUNKER_SUBSCRIPTION", "chunker-sub")
EXTRACTED_TEXT_BUCKET = "ingestion-extracted-text"
