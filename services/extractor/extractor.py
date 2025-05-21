import os
import tempfile
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
import logging

from shared.storage.gcs_client import download_file_from_gcs
from shared.pubsub.publisher import publish_event

OUTPUT_TOPIC = "ingestion-request"
GCS_BUCKET = os.getenv("GCS_BUCKET")


def extract_text_from_url(url: str) -> str:
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
        print("Received message:", message_dict)
        msg_type = message_dict.get("type")

        if msg_type == "url":
            tenant_id = message_dict.get("tenant_id")
            url_id = message_dict.get("url_id")
            url = message_dict.get("url")

            if not all([tenant_id, url_id, url]):
                print("[ERROR] Missing required fields in URL message:", message_dict)
                return

            print(f"[URL MODE] Processing URL: {url} for tenant {tenant_id} with ID {url_id}")
            text = extract_text_from_url(url)
            print(f"[INFO] Extracted text (first 100 chars): {text[:100]}")

            publish_event(
                OUTPUT_TOPIC,
                {
                    "document_id": url_id,
                    "text": text,
                    "tenant_id": tenant_id,
                    "filename": url,  # Using URL as identifier
                }
            )
            print("[INFO] URL extraction completed and event published.")
            return

        elif msg_type == "file":
            print("[FILE MODE] Processing file upload")
            tenant_id = message_dict.get("tenant_id")
            file_id = message_dict.get("file_id")
            gcs_path = message_dict.get("gcs_path")

            if not all([tenant_id, file_id, gcs_path]):
                print("[ERROR] Missing required fields in file message:", message_dict)
                return

            bucket = GCS_BUCKET or "your-bucket-name"
            file_path = gcs_path
            document_id = file_id

            print(f"[INFO] Processing file {file_path} from bucket {bucket} (document {document_id})")

            text = extract_text_from_pdf(file_path)
            print(f"[INFO] Extracted text (first 100 chars): {text[:100]}")

            publish_event(
                OUTPUT_TOPIC,
                {
                    "document_id": document_id,
                    "text": text,
                    "tenant_id": tenant_id,
                    "filename": message_dict.get("filename"),
                }
            )
            print("[INFO] File extraction completed and event published.")
            return

        print("[INFO] Unknown message type, skipping.")

    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")
