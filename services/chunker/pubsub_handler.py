from chunking import chunk_text

from shared.pubsub.publisher import publish_event


def handle_extracted_text_message(payload: dict):
    document_id = payload["document_id"]
    tenant_id = payload["tenant_id"]
    text = payload["text"]
    chunk_size = payload.get("chunk_size", 1000)
    chunk_overlap = payload.get("chunk_overlap", 200)

    chunks = chunk_text(
        text=text,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        tenant_id=tenant_id,
        document_id=document_id,
    )

    for chunk in chunks:
        publish_event("embedding-topic", chunk)
