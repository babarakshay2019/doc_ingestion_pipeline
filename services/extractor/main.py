from shared.pubsub.subscriber import subscribe_to_topic
from extractor import handle_ingestion_event

if __name__ == "__main__":
    # Subscribe to Pub/Sub and process incoming messages
    subscribe_to_topic(
        topic="ingestion-request",
        subscription="extractor-sub",
        callback=handle_ingestion_event
    )
