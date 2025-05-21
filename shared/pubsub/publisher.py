from google.cloud import pubsub_v1
import os
import json

PROJECT_ID = os.getenv("GCP_PROJECT")

def publish_event(topic: str, payload: dict):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, topic)
    future = publisher.publish(topic_path, data=json.dumps(payload).encode("utf-8"))
    return future.result()

