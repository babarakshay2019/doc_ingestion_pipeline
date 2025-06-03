import os
import tempfile
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
import logging
from config import PUBSUB_TOPIC, GCS_BUCKET

from shared.storage.gcs_client import download_file_from_gcs
from shared.pubsub.publisher import publish_event


# Configure logging: timestamp, level, message
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def extract_text_from_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url  # default to https

    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts and styles for cleaner text
    for script in soup(["script", "style"]):
        script.decompose()

    # Return cleaned and visible text
    return soup.get_text(separator="\n", strip=True)


def extract_text_from_pdf(gcs_path: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        download_file_from_gcs(gcs_path, tmp_file.name)
        doc = fitz.open(tmp_file.name)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
    return text


def handle_ingestion_event(message_dict: dict):
    try:
        logger.info("Received message: %s", message_dict)
        msg_type = message_dict.get("type")

        if msg_type == "url":
            tenant_id = message_dict.get("tenant_id")
            url_id = message_dict.get("url_id")
            url = message_dict.get("url")

            if not all([tenant_id, url_id, url]):
                logger.error("Missing required fields in URL message: %s", message_dict)
                return

            logger.info("Processing URL: %s for tenant %s with ID %s", url, tenant_id, url_id)
            text = extract_text_from_url(url)
            logger.info("Extracted text (first 100 chars): %s", text[:100])

            publish_event(
                PUBSUB_TOPIC,
                {
                    "document_id": url_id,
                    "text": text,
                    "tenant_id": tenant_id,
                    "filename": url,  # Using URL as identifier
                }
            )
            logger.info("URL extraction completed and event published.")
            return

        elif msg_type == "file":
            logger.info("Processing file upload")
            tenant_id = message_dict.get("tenant_id")
            file_id = message_dict.get("file_id")
            gcs_path = message_dict.get("gcs_path")

            if not all([tenant_id, file_id, gcs_path]):
                logger.error("Missing required fields in file message: %s", message_dict)
                return

            bucket = GCS_BUCKET 
            file_path = gcs_path
            document_id = file_id

            logger.info("Processing file %s from bucket %s (document %s)", file_path, bucket, document_id)

            text = extract_text_from_pdf(file_path)
            logger.info("Extracted text (first 100 chars): %s", text[:100])

            publish_event(
                PUBSUB_TOPIC,
                {
                    "document_id": document_id,
                    "text": text,
                    "tenant_id": tenant_id,
                    "filename": message_dict.get("filename"),
                }
            )
            logger.info("File extraction completed and event published.")
            return

        logger.info("Unknown message type, skipping.")

    except Exception as e:
        logger.error("Extraction failed: %s", e, exc_info=True)
