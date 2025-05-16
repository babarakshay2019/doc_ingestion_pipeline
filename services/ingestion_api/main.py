# services/ingestion_api/main.py
from fastapi import FastAPI
from api import router

app = FastAPI(title="Ingestion API")

app.include_router(router, prefix="/api")
