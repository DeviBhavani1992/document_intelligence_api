from fastapi import FastAPI
from dotenv import load_dotenv
import os

# 🔴 THIS LINE IS THE KEY
load_dotenv()

from app.api.router import router as api_router

app = FastAPI(title="Document Intelligence API")

app.include_router(api_router)

@app.get("/")
def root():
    return {"status": "running"}
