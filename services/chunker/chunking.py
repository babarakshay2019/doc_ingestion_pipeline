from typing import List, Dict
import uuid

def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    tenant_id: str = "default",
    document_id: str = "unknown"
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
            "end_offset": end
        }
        chunks.append(chunk_data)
        start += chunk_size - chunk_overlap
        index += 1
    return chunks
