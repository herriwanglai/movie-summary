# Agent 2: Backend API & Upload System

## Role
Backend developer building METEORA LX FastAPI server with chunked video upload system and database integration.

## Primary Responsibility
Create a robust FastAPI backend that handles chunked video uploads, stores metadata in a database, and triggers video processing.

## Tech Stack
- **Framework:** FastAPI (Python 3.11+)
- **ORM:** SQLAlchemy 2.0
- **Migrations:** Alembic
- **Database:** SQLite (dev) or PostgreSQL (prod)
- **Validation:** Pydantic v2
- **File Handling:** python-multipart, aiofiles
- **CORS:** fastapi-cors-middleware
- **Testing:** pytest, httpx

## Documentation Sub-Agent Responsibilities

### **Priority 1: FastAPI Best Practices**
- Learn FastAPI project structure (routers, models, schemas)
- Study async/await patterns in FastAPI
- Understand dependency injection
- Learn middleware configuration (CORS, logging)
- Study error handling and exception handlers
- Learn background tasks for long-running operations

### **Priority 2: Chunked File Upload Implementation**
- Study chunked upload algorithms
- Learn file reassembly strategies
- Understand upload session management
- Study resume/pause upload patterns
- Learn file integrity validation (checksums)
- Study cleanup strategies for failed uploads

### **Priority 3: SQLAlchemy 2.0 Patterns**
- Learn SQLAlchemy 2.0 syntax (new style)
- Study relationship patterns (one-to-many, many-to-many)
- Understand async database sessions
- Learn migration best practices with Alembic
- Study database indexing for performance
- Learn query optimization techniques

### **Priority 4: Pydantic v2 Validation**
- Learn Pydantic v2 model syntax
- Study custom validators
- Understand serialization/deserialization
- Learn config settings management
- Study file upload validation patterns

### **Priority 5: API Security & Performance**
- Study rate limiting implementation
- Learn file upload size limits
- Understand CORS configuration
- Study request validation
- Learn async file I/O optimization

## Key Implementation Tasks

### **Task 1: FastAPI Project Setup** (1 hour)

**Project Structure:**
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Settings with Pydantic
│   ├── database.py          # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── video.py         # SQLAlchemy models
│   │   ├── scene.py
│   │   ├── screenshot.py
│   │   └── annotation.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── video.py         # Pydantic schemas
│   │   ├── upload.py
│   │   └── response.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── upload.py        # Upload endpoints
│   │   ├── videos.py        # Video CRUD
│   │   └── health.py        # Health check
│   ├── services/
│   │   ├── __init__.py
│   │   ├── upload_service.py
│   │   └── video_service.py
│   └── utils/
│       ├── __init__.py
│       └── file_utils.py
├── alembic/                 # Database migrations
├── uploads/                 # Temporary upload chunks
├── videos/                  # Final video storage
├── requirements.txt
└── .env.example
```

**Files to Create:**

**`backend/requirements.txt`:**
```
fastapi==0.110.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
alembic==1.13.1
pydantic==2.6.0
pydantic-settings==2.1.0
python-multipart==0.0.9
aiofiles==23.2.1
python-dotenv==1.0.0
psycopg2-binary==2.9.9  # For PostgreSQL
```

**`backend/app/config.py`:**
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "METEORA LX API"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"

    DATABASE_URL: str = "sqlite:///./meteora_lx.db"

    # Upload settings
    UPLOAD_DIR: str = "uploads"
    VIDEO_DIR: str = "videos"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024 * 1024  # 10GB
    CHUNK_SIZE: int = 5 * 1024 * 1024  # 5MB

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
```

**Success Criteria:**
- FastAPI app starts without errors
- Project structure follows best practices
- Environment variables loaded correctly
- CORS configured for frontend origin

---

### **Task 2: Database Models** (1-2 hours)

**File:** `backend/app/models/video.py`

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_path = Column(String, unique=True)
    file_size = Column(Integer)
    duration = Column(Float, nullable=True)
    mime_type = Column(String)

    # Processing status
    status = Column(String, default="uploaded")  # uploaded, processing, completed, error
    processing_progress = Column(Float, default=0.0)

    # Metadata
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    fps = Column(Float, nullable=True)
    codec = Column(String, nullable=True)

    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)

    # Relationships
    scenes = relationship("Scene", back_populates="video", cascade="all, delete-orphan")
    screenshots = relationship("Screenshot", back_populates="video", cascade="all, delete-orphan")
    clips = relationship("Clip", back_populates="video", cascade="all, delete-orphan")

class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))

    start_time = Column(Float)
    end_time = Column(Float)
    duration = Column(Float)

    # Importance metrics
    importance_score = Column(Float, default=0.0)
    visual_intensity = Column(Float, default=0.0)
    audio_intensity = Column(Float, default=0.0)
    dialogue_density = Column(Float, default=0.0)

    # Description
    description = Column(Text, nullable=True)

    video = relationship("Video", back_populates="scenes")
    keyframes = relationship("Keyframe", back_populates="scene", cascade="all, delete-orphan")

class Keyframe(Base):
    __tablename__ = "keyframes"

    id = Column(Integer, primary_key=True, index=True)
    scene_id = Column(Integer, ForeignKey("scenes.id"))

    timestamp = Column(Float)
    image_path = Column(String)

    scene = relationship("Scene", back_populates="keyframes")
```

**File:** `backend/app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Alembic Setup:**
```bash
cd backend
alembic init alembic
# Edit alembic.ini to use database URL
# Create first migration
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

**Success Criteria:**
- Database tables created successfully
- Relationships work correctly
- Migrations run without errors

---

### **Task 3: Chunked Upload System** (3-4 hours)

**File:** `backend/app/routers/upload.py`

```python
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
import os
import uuid
import aiofiles
from app.database import get_db
from app.models.video import Video
from app.schemas.upload import InitUploadResponse, ChunkUploadResponse, CompleteUploadResponse
from app.config import settings

router = APIRouter(prefix="/upload", tags=["upload"])

# In-memory upload session storage (use Redis in production)
upload_sessions = {}

@router.post("/init", response_model=InitUploadResponse)
async def init_upload(
    filename: str = Form(...),
    file_size: int = Form(...),
    mime_type: str = Form(...)
):
    """Initialize a chunked upload session"""

    # Validate file size
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    # Validate mime type
    allowed_types = ["video/mp4", "video/quicktime", "video/x-matroska", "video/webm"]
    if mime_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Generate upload ID
    upload_id = str(uuid.uuid4())

    # Calculate number of chunks
    chunk_count = (file_size + settings.CHUNK_SIZE - 1) // settings.CHUNK_SIZE

    # Create upload directory
    upload_dir = os.path.join(settings.UPLOAD_DIR, upload_id)
    os.makedirs(upload_dir, exist_ok=True)

    # Store session
    upload_sessions[upload_id] = {
        "filename": filename,
        "file_size": file_size,
        "mime_type": mime_type,
        "chunk_count": chunk_count,
        "chunks_uploaded": set(),
        "upload_dir": upload_dir
    }

    return InitUploadResponse(
        upload_id=upload_id,
        chunk_size=settings.CHUNK_SIZE,
        chunk_count=chunk_count
    )

@router.post("/chunk", response_model=ChunkUploadResponse)
async def upload_chunk(
    upload_id: str = Form(...),
    chunk_index: int = Form(...),
    chunk: UploadFile = File(...)
):
    """Upload a single chunk"""

    # Validate upload session
    if upload_id not in upload_sessions:
        raise HTTPException(status_code=404, detail="Upload session not found")

    session = upload_sessions[upload_id]

    # Validate chunk index
    if chunk_index >= session["chunk_count"]:
        raise HTTPException(status_code=400, detail="Invalid chunk index")

    # Save chunk to disk
    chunk_path = os.path.join(session["upload_dir"], f"chunk_{chunk_index}")

    async with aiofiles.open(chunk_path, 'wb') as f:
        content = await chunk.read()
        await f.write(content)

    # Mark chunk as uploaded
    session["chunks_uploaded"].add(chunk_index)

    # Calculate progress
    progress = len(session["chunks_uploaded"]) / session["chunk_count"] * 100

    return ChunkUploadResponse(
        chunk_index=chunk_index,
        progress=progress,
        chunks_uploaded=len(session["chunks_uploaded"]),
        total_chunks=session["chunk_count"]
    )

@router.post("/complete", response_model=CompleteUploadResponse)
async def complete_upload(
    upload_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """Complete upload by reassembling chunks"""

    # Validate upload session
    if upload_id not in upload_sessions:
        raise HTTPException(status_code=404, detail="Upload session not found")

    session = upload_sessions[upload_id]

    # Validate all chunks uploaded
    if len(session["chunks_uploaded"]) != session["chunk_count"]:
        raise HTTPException(
            status_code=400,
            detail=f"Missing chunks: {session['chunk_count'] - len(session['chunks_uploaded'])}"
        )

    # Reassemble file
    final_filename = f"{uuid.uuid4()}_{session['filename']}"
    final_path = os.path.join(settings.VIDEO_DIR, final_filename)

    async with aiofiles.open(final_path, 'wb') as outfile:
        for i in range(session["chunk_count"]):
            chunk_path = os.path.join(session["upload_dir"], f"chunk_{i}")
            async with aiofiles.open(chunk_path, 'rb') as infile:
                chunk_data = await infile.read()
                await outfile.write(chunk_data)

    # Create database record
    video = Video(
        filename=session["filename"],
        file_path=final_path,
        file_size=session["file_size"],
        mime_type=session["mime_type"],
        status="uploaded"
    )
    db.add(video)
    db.commit()
    db.refresh(video)

    # Cleanup chunks
    import shutil
    shutil.rmtree(session["upload_dir"])

    # Remove session
    del upload_sessions[upload_id]

    # TODO: Trigger video processing (Agent 3)
    # from app.services.processing import process_video
    # process_video.delay(video.id)  # Celery task or background task

    return CompleteUploadResponse(
        video_id=video.id,
        status="uploaded",
        message="Upload completed successfully"
    )
```

**Success Criteria:**
- Init endpoint returns upload_id
- Chunks upload successfully
- File reassembles correctly
- Database record created
- Chunk cleanup works

---

### **Task 4: Video CRUD Endpoints** (1 hour)

**File:** `backend/app/routers/videos.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.video import Video
from app.schemas.video import VideoResponse

router = APIRouter(prefix="/videos", tags=["videos"])

@router.get("/", response_model=List[VideoResponse])
def list_videos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all uploaded videos"""
    videos = db.query(Video).offset(skip).limit(limit).all()
    return videos

@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):
    """Get video by ID"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
```

---

### **Task 5: Health Check & Main App** (30 min)

**File:** `backend/app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import upload, videos, health
from app.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(upload.router, prefix=settings.API_PREFIX)
app.include_router(videos.router, prefix=settings.API_PREFIX)
```

**File:** `backend/app/routers/health.py`

```python
from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "METEORA LX API"}
```

---

## Integration Points

### **With Agent 1 (Frontend):**
- Provide OpenAPI spec at `/docs`
- Document all endpoints clearly
- Use consistent response formats
- Handle CORS properly

### **With Agent 3 (Video Processing):**
- Trigger processing after upload complete
- Update video status during processing
- Store processing results (scenes, keyframes)
- Handle processing errors

**Handoff:**
```python
# In complete_upload(), after creating video record:
from app.services.video_processor import process_video_task
process_video_task.delay(video.id)  # Background task
```

## Testing Checklist

- [ ] FastAPI app starts on port 8000
- [ ] Health check returns 200
- [ ] OpenAPI docs accessible at /docs
- [ ] CORS allows frontend origin
- [ ] Init upload returns upload_id
- [ ] Can upload chunks sequentially
- [ ] File reassembles correctly (verify checksum)
- [ ] Database stores video metadata
- [ ] List videos endpoint works
- [ ] Get video by ID works
- [ ] Chunk cleanup removes temporary files
- [ ] Large file uploads work (1GB+)

## Documentation Sub-Agent Deliverables

1. **FastAPI Quick Reference:**
   - Project structure example
   - Async endpoint patterns
   - Dependency injection examples

2. **Chunked Upload Guide:**
   - Algorithm explanation
   - File reassembly code
   - Session management pattern

3. **SQLAlchemy 2.0 Cheat Sheet:**
   - Model definition examples
   - Relationship patterns
   - Query examples

4. **Pydantic v2 Patterns:**
   - Schema examples
   - Validator examples
   - Config settings

## Success Criteria

Agent 2 is complete when:
1. ✅ FastAPI app runs without errors
2. ✅ Database schema created
3. ✅ Upload init endpoint works
4. ✅ Chunk upload endpoint works
5. ✅ Upload complete endpoint reassembles file
6. ✅ Video metadata stored in database
7. ✅ CORS configured correctly
8. ✅ API docs accessible
9. ✅ Code follows best practices
10. ✅ Integration ready for Agent 1 and Agent 3

## Estimated Timeline
- Project setup: **1 hour**
- Database models: **1-2 hours**
- Chunked upload: **3-4 hours**
- Video CRUD: **1 hour**
- Testing: **1 hour**

**Total: 7-9 hours**
