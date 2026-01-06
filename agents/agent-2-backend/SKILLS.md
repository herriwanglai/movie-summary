# Agent 2: Backend API & Upload System

## Role
Backend developer building METEORA LX FastAPI server with chunked video upload system and database integration.

## Primary Responsibility
Create a robust FastAPI backend that handles chunked video uploads, stores metadata in a database, and triggers video processing.

## Tech Stack
- **Framework:** FastAPI (Python 3.11+)
- **Upload:** tuspyserver (TUS resumable upload protocol)
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

### **Priority 2: TUS Protocol & tuspyserver**
- Learn TUS (resumable upload) protocol basics
- Study tuspyserver library API and configuration
- Understand upload completion hooks
- Learn TUS-specific CORS headers configuration
- Study metadata storage with TUS
- Learn cleanup and expiration settings

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
tuspyserver>=0.1.0  # TUS resumable upload protocol
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

    # Upload settings (TUS)
    VIDEO_DIR: str = "videos"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024 * 1024  # 10GB
    UPLOAD_RETENTION_DAYS: int = 5  # Auto-cleanup old uploads

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

### **Task 3: TUS Resumable Upload Integration** (30 minutes) ⚡

**Using tuspyserver library - drastically simplifies upload implementation!**

**File:** `backend/app/services/upload_handler.py`

```python
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.video import Video
from app.config import settings
import logging
import os

logger = logging.getLogger(__name__)

def handle_upload_complete(file_path: str, metadata: dict):
    """
    Triggered when TUS upload completes

    Args:
        file_path: Full path to uploaded video file
        metadata: Dict containing filename, filetype, etc.
    """
    logger.info(f"Upload complete: {file_path}")
    logger.info(f"Metadata: {metadata}")

    # Get filename and file info
    filename = metadata.get('filename', os.path.basename(file_path))
    file_size = os.path.getsize(file_path)
    mime_type = metadata.get('filetype', 'video/mp4')

    # Create database record
    db = SessionLocal()
    try:
        video = Video(
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
            status="uploaded"
        )
        db.add(video)
        db.commit()
        db.refresh(video)

        logger.info(f"Created video record with ID: {video.id}")

        # TODO: Trigger video processing (Agent 3)
        # from app.services.video_processor import process_video_task
        # process_video_task.delay(video.id)

        return video.id

    except Exception as e:
        logger.error(f"Failed to create video record: {e}")
        db.rollback()
        raise
    finally:
        db.close()
```

**File:** `backend/app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tuspyserver import create_tus_router
from app.config import settings
from app.routers import videos, health
from app.database import engine, Base
from app.services.upload_handler import handle_upload_complete

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
        # retention_days=settings.UPLOAD_RETENTION_DAYS  # Auto-cleanup
    ),
    prefix=f"{settings.API_PREFIX}/upload"
)

# Mount other routers
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(videos.router, prefix=settings.API_PREFIX)
```

**That's it!** 🎉 tuspyserver handles:
- ✅ Chunked upload protocol
- ✅ Resume/pause functionality
- ✅ Session management
- ✅ File reassembly
- ✅ Progress tracking
- ✅ Automatic cleanup
- ✅ Metadata storage

**Success Criteria:**
- TUS router mounted at `/api/upload`
- Upload completion hook creates video record
- File stored in VIDEO_DIR
- Database record created
- Ready for frontend TUS client integration

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
- [ ] TUS router mounted at /api/upload
- [ ] Can upload video via TUS protocol
- [ ] Upload completion hook triggers
- [ ] Database stores video metadata
- [ ] List videos endpoint works
- [ ] Get video by ID works
- [ ] Large file uploads work (1GB+)
- [ ] Resume/pause upload works (TUS feature)

## Documentation Sub-Agent Deliverables

1. **FastAPI Quick Reference:**
   - Project structure example
   - Async endpoint patterns
   - Dependency injection examples

2. **TUS Protocol Guide:**
   - TUS protocol overview
   - tuspyserver API reference
   - Upload completion hook examples

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
3. ✅ TUS upload router mounted and working
4. ✅ Upload completion hook creates video records
5. ✅ Resume/pause upload functionality works
6. ✅ Video metadata stored in database
7. ✅ CORS configured correctly (including TUS headers)
8. ✅ API docs accessible
9. ✅ Code follows best practices
10. ✅ Integration ready for Agent 1 and Agent 3

## Estimated Timeline
- Project setup: **1 hour**
- Database models: **1-2 hours**
- TUS upload integration: **30 minutes** ⚡ (was 3-4 hours with custom implementation!)
- Video CRUD: **1 hour**
- Testing: **1 hour**

**Total: 4.5-5.5 hours** (down from 7-9 hours!)

**Time saved by using tuspyserver: 2.5-3.5 hours!** 🎉
