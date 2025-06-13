# services/ingestion_api/api.py
import tempfile
import uuid

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from utils import publish_ingestion_event, save_file_to_gcs

from config import EXTRACTED_TEXT_BUCKET
from services.extractor.extractor import (extract_text_from_pdf,
                                          extract_text_from_url)

router = APIRouter()


@router.post("/upload")
async def upload_file(tenant_id: str = Form(...), file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        gcs_path = await save_file_to_gcs(file, tenant_id, file_id)

        # Construct future public URL for extracted output
        extracted_blob_name = f"file/{file_id}.json"
        public_url = f"https://storage.googleapis.com/{EXTRACTED_TEXT_BUCKET}/{extracted_blob_name}"

        # Publish event to extractor
        await publish_ingestion_event(
            {
                "type": "file",
                "tenant_id": tenant_id,
                "file_id": file_id,
                "filename": file.filename,
                "gcs_path": gcs_path,
            }
        )

        return JSONResponse(
            {"status": "success", "file_id": file_id, "expected_extracted_url": public_url}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/url")
async def submit_url(tenant_id: str = Form(...), url: str = Form(...)):
    try:
        url_id = str(uuid.uuid4())

        # Construct future public URL for extracted output
        extracted_blob_name = f"url/{url_id}.json"
        public_url = f"https://storage.googleapis.com/{EXTRACTED_TEXT_BUCKET}/{extracted_blob_name}"

        # Publish event to extractor
        await publish_ingestion_event(
            {"type": "url", "tenant_id": tenant_id, "url_id": url_id, "url": url}
        )

        return JSONResponse(
            {"status": "success", "url_id": url_id, "expected_extracted_url": public_url}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract/direct-file")
async def extract_direct_file(tenant_id: str = Form(...), file: UploadFile = File(...)):
    try:
        # Save uploaded file to a temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        # This is a local file, not from GCS
        extracted_text = extract_text_from_pdf(tmp_path, from_gcs=False)

        return JSONResponse({"extracted_text": extracted_text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract/direct-url")
async def extract_direct_url(tenant_id: str = Form(...), url: str = Form(...)):
    try:
        extracted_text = extract_text_from_url(url)
        return JSONResponse({"extracted_text": extracted_text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
