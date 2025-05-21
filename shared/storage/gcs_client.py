from google.cloud import storage
import os

BUCKET = os.getenv("GCS_BUCKET")

def download_file_from_gcs(gcs_path: str, local_path: str):
    from google.cloud import storage
    import os

    BUCKET = os.getenv("GCS_BUCKET")
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET)
    blob = bucket.blob(gcs_path)
    blob.download_to_filename(local_path)


