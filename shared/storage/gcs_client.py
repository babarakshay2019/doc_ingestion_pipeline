import json
import logging

from google.cloud import storage

from config import EXTRACTED_TEXT_BUCKET, GCS_BUCKET

logger = logging.getLogger(__name__)


def download_file_from_gcs(gcs_path: str, local_path: str):
    try:
        logger.info(f"Downloading from GCS path: {gcs_path} to local path: {local_path}")
        storage_client = storage.Client()
        bucket = storage_client.bucket(GCS_BUCKET)

        blob = bucket.blob(gcs_path)
        if not blob.exists():
            logger.error(f" Blob not found in bucket '{GCS_BUCKET}': {gcs_path}")
            return

        blob.download_to_filename(local_path)
        logger.info(f" Successfully downloaded {gcs_path} to {local_path}")
    except Exception as e:
        logger.error(f"Error downloading file from GCS: {e}", exc_info=True)


def upload_extracted_text_to_gcs(blob_name: str, content: dict) -> str:
    try:
        logger.info(f"Uploading extracted content to GCS: {blob_name}")

        client = storage.Client()
        bucket = client.bucket(EXTRACTED_TEXT_BUCKET)
        blob = bucket.blob(blob_name)

        # Upload content as JSON
        blob.upload_from_string(
            json.dumps(content, ensure_ascii=False), content_type="application/json"
        )

        # Make the object publicly accessible for read-only
        blob.make_public()

        # Use GCS-generated public URL
        public_url = blob.public_url

        logger.info(f"Uploaded to GCS: {public_url}")
        return public_url

    except Exception:
        logger.error("Failed to upload extracted text to GCS", exc_info=True)
        return ""
