import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, upload, analysis

# Initialize FastAPI App
app = FastAPI(
    title="QCR AI – Quality Control Record Discrepancy Detection System",
    description="SIH 2026 Hackathon Core Backend Engine",
    version="1.0.0"
)

# CORS Policy Configuration
# Allows React frontend running on port 5173 to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Endpoint Routers
app.include_router(health.router, prefix="/health", tags=["Health Checks"])
app.include_router(upload.router, prefix="/upload", tags=["Ingestion & OCR"])
app.include_router(analysis.router, prefix="", tags=["Discrepancy Engine"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
