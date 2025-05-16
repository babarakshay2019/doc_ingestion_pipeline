#  core event handling
import os
from shared.storage.gcs_client import download_file_from_gcs
from shared.pubsub.publisher import publish_event
from utils.text_extractors import extract_text_from_file, extract_text_from_url

def handle_ingestion_event(payload: dict):
    if payload["type"] == "file":
        file_path = download_file_from_gcs(payload["gcs_path"])
        text = extract_text_from_file(file_path)
    elif payload["type"] == "url":
        text = extract_text_from_url(payload["url"])
    else:
        raise ValueError("Unsupported ingestion type")

    publish_event("extraction-complete", {
        "tenant_id": payload["tenant_id"],
        "source_id": payload.get("file_id") or payload.get("url_id"),
        "text": text
    })
