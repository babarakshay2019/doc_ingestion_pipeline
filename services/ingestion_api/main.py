# services/ingestion_api/main.py
from api import router
from fastapi import FastAPI

app = FastAPI(title="Ingestion API")

app.include_router(router, prefix="/api")
