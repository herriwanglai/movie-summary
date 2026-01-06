# METEORA LX - Backend API

FastAPI backend with TUS resumable uploads for the METEORA LX video summarization platform.

## Features

- **TUS Resumable Uploads**: Chunked video upload protocol with pause/resume support
- **RESTful API**: Video CRUD operations
- **SQLAlchemy 2.0**: Modern ORM with Alembic migrations
- **FastAPI**: High-performance async web framework
- **OpenAPI Documentation**: Auto-generated API docs at `/docs`

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Settings with Pydantic
│   ├── database.py          # Database connection
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── video.py         # Video, Scene, Keyframe, Screenshot, Clip
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   └── video.py         # Request/response schemas
│   ├── routers/             # API endpoints
│   │   ├── __init__.py
│   │   ├── health.py        # Health check
│   │   └── videos.py        # Video CRUD
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── upload_handler.py # TUS completion hook
│   └── utils/
│       └── __init__.py
├── alembic/                 # Database migrations
├── uploads/                 # Temporary upload chunks
├── videos/                  # Final video storage
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run Migrations

```bash
alembic upgrade head
```

### 5. Start Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Health Check
- `GET /api/health` - Check API status

### Videos
- `GET /api/videos/` - List all videos
- `GET /api/videos/{id}` - Get video by ID

### TUS Upload
- `POST /api/upload/files/` - Create upload session
- `OPTIONS /api/upload/files/` - Get TUS capabilities
- `HEAD /api/upload/files/{uuid}` - Check upload status
- `PATCH /api/upload/files/{uuid}` - Upload chunk
- `DELETE /api/upload/files/{uuid}` - Cancel upload

### Documentation
- `GET /docs` - OpenAPI/Swagger UI
- `GET /redoc` - ReDoc documentation
- `GET /openapi.json` - OpenAPI schema

## Database Models

### Video
- Stores uploaded video metadata
- Tracks processing status
- Links to scenes, keyframes, screenshots, clips

### Scene
- Represents a detected scene in the video
- Includes importance metrics
- Links to keyframes

### Keyframe
- Key frame images extracted from scenes
- Timestamp and image path

### Screenshot
- User-generated screenshots
- Timestamp and optional description

### Clip
- Extracted video clips
- Start/end time, title, description

## Configuration

Environment variables (see `.env.example`):

```bash
PROJECT_NAME="METEORA LX API"
VERSION="0.1.0"
API_PREFIX="/api"
DATABASE_URL="sqlite:///./meteora_lx.db"
VIDEO_DIR="videos"
MAX_UPLOAD_SIZE=10737418240  # 10GB
UPLOAD_RETENTION_DAYS=5
CORS_ORIGINS=["http://localhost:3000"]
```

## Development

### Run Tests
```bash
pytest
```

### Create Migration
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Format Code
```bash
black app/
```

## TUS Protocol

The backend uses the TUS resumable upload protocol:

1. **Create Upload**: POST to `/api/upload/files/` with metadata
2. **Upload Chunks**: PATCH with binary data
3. **Resume**: Check offset with HEAD, continue with PATCH
4. **Completion**: Automatic callback to `handle_upload_complete()`

The completion hook:
- Saves video metadata to database
- Triggers video processing pipeline (Agent 3)
- Returns video ID

## CORS Configuration

TUS-specific headers are exposed for cross-origin requests:
- `Location` - Upload URL
- `Upload-Offset` - Current progress
- `Tus-Resumable` - Protocol version
- `Upload-Length` - Total size

## Integration Points

### Frontend (Agent 1)
- Consume REST API endpoints
- Use TUS client library for uploads
- Check OpenAPI docs at `/docs`

### Video Processor (Agent 3)
- Triggered from `upload_handler.py`
- Processes uploaded videos
- Updates database with results

## Success Criteria

- ✅ FastAPI runs on port 8000
- ✅ TUS router at `/api/upload/files/`
- ✅ Database tables created
- ✅ Upload completion hook works
- ✅ CORS configured
- ✅ OpenAPI docs at `/docs`
- ✅ All endpoints tested and working

## Tech Stack

- **FastAPI** 0.110.0 - Web framework
- **tuspyserver** 4.2.3 - TUS protocol implementation
- **SQLAlchemy** 2.0.25 - ORM
- **Alembic** 1.13.1 - Database migrations
- **Pydantic** 2.6.0 - Data validation
- **Uvicorn** 0.27.0 - ASGI server

## License

MIT
