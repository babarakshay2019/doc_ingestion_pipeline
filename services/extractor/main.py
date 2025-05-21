import logging
import sys
import signal
import os
from dotenv import load_dotenv

from shared.pubsub.subscriber import subscribe_to_topic
from extractor import handle_ingestion_event

# Load .env variables (e.g., local dev or Docker secrets)
load_dotenv()

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(name)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Graceful shutdown handler
def shutdown_handler(signum, frame):
    logger.info("Shutdown signal received. Exiting gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    # Register termination signals
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    # Load from environment or fall back to defaults
    topic = os.getenv("PUBSUB_TOPIC", "ingestion-request")
    subscription = os.getenv("SUBSCRIPTION_NAME", "extractor-sub")

    logger.info(f"Starting extractor service...")
    logger.info(f"Subscribing to topic '{topic}' with subscription '{subscription}'")

    # Begin subscription loop
    subscribe_to_topic(
        topic=topic,
        subscription=subscription,
        callback=handle_ingestion_event,
        raw_message=False
    )