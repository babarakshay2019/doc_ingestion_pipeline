from typing import List, Dict
import uuid
from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
    tenant_id: str = "default",
    document_id: str = "unknown",
) -> List[Dict]:
    chunks = []
    start = 0
    index = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunk_data = {
            "chunk_id": str(uuid.uuid4()),
            "tenant_id": tenant_id,
            "document_id": document_id,
            "chunk_text": chunk,
            "chunk_index": index,
            "start_offset": start,
            "end_offset": end,
        }
        chunks.append(chunk_data)
        start += chunk_size - chunk_overlap
        index += 1
    return chunks
