# services/ingestion_api/utils.py
from google.cloud import storage, pubsub_v1
import os
import json
import aiofiles

GCS_BUCKET = os.getenv("GCS_BUCKET")
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC")
PROJECT_ID = os.getenv("GCP_PROJECT")

async def save_file_to_gcs(file, tenant_id, file_id):
    path = f"{tenant_id}/{file_id}_{file.filename}"
    local_path = f"/tmp/{file_id}_{file.filename}"

    async with aiofiles.open(local_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET)
    blob = bucket.blob(path)
    blob.upload_from_filename(local_path)

    return path

async def publish_ingestion_event(payload: dict):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, PUBSUB_TOPIC)
    future = publisher.publish(
        topic_path,
        data=json.dumps(payload).encode("utf-8"),
        **{"content-type": "application/json"}
    )
    return future.result()
