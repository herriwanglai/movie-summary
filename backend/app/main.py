from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tuspyserver import create_tus_router
from app.config import settings
from app.routers import videos, health
from app.database import engine, Base
from app.services.upload_handler import handle_upload_complete
import os

# Ensure upload directories exist
os.makedirs(settings.VIDEO_DIR, exist_ok=True)
os.makedirs("uploads", exist_ok=True)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# CORS with TUS-specific headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "Location",           # TUS: Upload URL
        "Upload-Offset",      # TUS: Current upload progress
        "Tus-Resumable",      # TUS: Protocol version
        "Tus-Version",        # TUS: Supported versions
        "Tus-Extension",      # TUS: Supported extensions
        "Tus-Max-Size",       # TUS: Max upload size
        "Upload-Expires",     # TUS: Upload expiration
        "Upload-Length"       # TUS: Total upload size
    ],
)

# Mount TUS upload router
app.include_router(
    create_tus_router(
        files_dir=settings.VIDEO_DIR,
        on_upload_complete=handle_upload_complete,
        max_size=settings.MAX_UPLOAD_SIZE,
    ),
    prefix=f"{settings.API_PREFIX}/upload"
)

# Mount other routers
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(videos.router, prefix=settings.API_PREFIX)


@app.get("/")
def root():
    return {
        "message": "METEORA LX API",
        "version": settings.VERSION,
        "docs": "/docs"
    }
