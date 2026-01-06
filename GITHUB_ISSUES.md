# GitHub Issues - METEORA LX Critical & High Priority Fixes

**Generated from Comprehensive Code Review**
**Date:** January 6, 2026
**Total Issues:** 15 Critical + High Priority items

---

## 🔴 CRITICAL PRIORITY (Must Fix Before Production)

### Issue #1: [SECURITY] Path Traversal Vulnerability in Video Streaming

**Priority:** 🔴 Critical
**Type:** Security Vulnerability
**Effort:** 30 minutes
**Component:** Backend API

**Description:**
The video streaming endpoint does not validate file paths, allowing potential arbitrary file read if the database is compromised or file_path is manipulated.

**Affected File:**
`backend/app/routers/videos.py` lines 99-113

**Current Code:**
```python
@router.get("/{video_id}/stream")
def stream_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(
        video.file_path,  # ⚠️ No validation!
        media_type=video.mime_type,
        filename=video.filename
    )
```

**Security Impact:**
- Arbitrary file read if `file_path` is compromised
- Could expose system files, credentials, source code
- CWE-22: Improper Limitation of a Pathname to a Restricted Directory

**Recommended Fix:**
```python
from pathlib import Path

@router.get("/{video_id}/stream")
async def stream_video(video_id: int, db: AsyncSession = Depends(get_db)):
    video = await db.get(Video, video_id)
    if not video:
        raise HTTPException(404, "Video not found")

    # Validate path is within VIDEO_DIR
    video_dir = Path(settings.VIDEO_DIR).resolve()
    file_path = Path(video.file_path).resolve()

    if not file_path.is_relative_to(video_dir):
        logger.warning(f"Path traversal attempt: {video.file_path}")
        raise HTTPException(403, "Access denied")

    if not file_path.exists():
        raise HTTPException(404, "File not found")

    return FileResponse(
        str(file_path),
        media_type=video.mime_type,
        filename=secure_filename(video.filename)
    )
```

**Testing:**
```python
def test_path_traversal_prevention():
    # Try to access /etc/passwd
    video = Video(file_path="../../../etc/passwd")
    # Should raise HTTPException(403)
```

**Acceptance Criteria:**
- [ ] Path validation implemented
- [ ] Only files within VIDEO_DIR can be served
- [ ] Logged security warning for traversal attempts
- [ ] Unit test for path traversal prevention
- [ ] Verified with security scanner

---

### Issue #2: [SECURITY] No Authentication - API Completely Open

**Priority:** 🔴 Critical
**Type:** Security Gap
**Effort:** 8-12 hours
**Component:** Backend API, Frontend

**Description:**
The entire API is publicly accessible with no authentication or authorization. Anyone can upload, view, delete videos.

**Security Impact:**
- Unauthorized access to all videos
- Potential abuse (unlimited uploads)
- No user ownership tracking
- GDPR/privacy concerns
- Resource exhaustion attacks

**Recommended Implementation:**

**Backend - JWT Authentication:**
```python
# backend/app/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta

security = HTTPBearer()
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(401, "Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(401, "Invalid token")

# Protect endpoints
@router.post("/api/videos/")
async def create_video(
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Now user_id is verified
    ...
```

**Frontend - Token Management:**
```typescript
// frontend/src/lib/auth.ts
export const authStore = create<AuthState>((set) => ({
  token: localStorage.getItem('token'),
  user: null,

  login: async (email: string, password: string) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    const { access_token, user } = await response.json()
    localStorage.setItem('token', access_token)
    set({ token: access_token, user })
  },

  logout: () => {
    localStorage.removeItem('token')
    set({ token: null, user: null })
  }
}))

// Add to fetch calls
const response = await fetch('/api/videos', {
  headers: {
    'Authorization': `Bearer ${authStore.getState().token}`
  }
})
```

**Database Schema:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE videos ADD COLUMN user_id INTEGER REFERENCES users(id);
CREATE INDEX idx_videos_user_id ON videos(user_id);
```

**Acceptance Criteria:**
- [ ] User registration endpoint implemented
- [ ] User login endpoint with JWT tokens
- [ ] Password hashing (bcrypt/argon2)
- [ ] All video endpoints require authentication
- [ ] Videos associated with user ownership
- [ ] Token refresh mechanism
- [ ] Frontend login/logout UI
- [ ] Protected routes in frontend

**Subtasks:**
- [ ] Install dependencies: `pip install python-jose[cryptography] passlib[bcrypt]`
- [ ] Create User model in database
- [ ] Implement auth router (`/api/auth/login`, `/api/auth/register`)
- [ ] Add authentication dependency to video routes
- [ ] Add user_id foreign key to videos table
- [ ] Create Alembic migration
- [ ] Frontend: Auth context/store
- [ ] Frontend: Login/Register components
- [ ] Frontend: Token interceptor for API calls

---

### Issue #3: [BUG] Broken Video Processing - TypeError in Pipeline

**Priority:** 🔴 Critical
**Type:** Bug
**Effort:** 2 hours
**Component:** Backend - Video Processing

**Description:**
Video processing will fail immediately with TypeError due to incorrect parameter passing to VideoProcessingPipeline constructor.

**Affected File:**
`backend/app/services/video_processor.py` lines 39-43

**Error:**
```python
pipeline = VideoProcessingPipeline(
    video_path=video.file_path,
    scene_threshold=30.0,      # ❌ Constructor doesn't accept this
    keyframes_per_scene=3      # ❌ Constructor doesn't accept this
)
# TypeError: __init__() got unexpected keyword argument 'scene_threshold'
```

**Actual Pipeline Constructor:**
```python
# src/video_processor/pipeline.py line 18
def __init__(self, video_path: str):
    # Only accepts video_path!
```

**Fix:**
```python
# Create pipeline with just video_path
pipeline = VideoProcessingPipeline(video_path=video.file_path)

# Pass parameters to process() method instead
result = pipeline.process(
    scene_threshold=30.0,
    keyframes_per_scene=3,
    keyframe_method="middle"
)
```

**Also Fix Schema Mismatch:**
```python
# Current code references fields that don't exist
scene = Scene(
    video_id=video.id,
    start_frame=scene_data['start_frame'],  # ❌ Model doesn't have this field
    end_frame=scene_data['end_frame'],      # ❌ Model doesn't have this field
    # ...
)

# Fix: Use actual model fields
scene = Scene(
    video_id=video.id,
    start_time=scene_data['start_time'],
    end_time=scene_data['end_time'],
    importance_score=scene_data.get('importance_score', 0.5),
)
```

**Acceptance Criteria:**
- [ ] Pipeline initialized with correct parameters
- [ ] Processing parameters passed to process() method
- [ ] Scene model fields match database schema
- [ ] Keyframe model fields match database schema
- [ ] End-to-end video upload → process → complete works
- [ ] Integration test with real video file
- [ ] Error handling for processing failures

**Testing:**
```python
def test_video_processing_pipeline():
    video = create_test_video()
    result = process_video(video.id)

    assert result is not None
    assert video.status == "completed"
    assert Scene.query.filter_by(video_id=video.id).count() > 0
```

---

### Issue #4: [CRITICAL] Dangerous Daemon Thread Processing - Data Corruption Risk

**Priority:** 🔴 Critical
**Type:** Architecture Flaw
**Effort:** 8 hours
**Component:** Backend - Background Processing

**Description:**
Video processing uses daemon threads which are killed on shutdown without cleanup, risking data corruption and lost work.

**Affected File:**
`backend/app/services/video_processor.py` lines 111-119

**Current Code:**
```python
def process_video_async(video_id: int):
    """Process video asynchronously (for background tasks)"""
    import threading
    thread = threading.Thread(target=process_video, args=(video_id,))
    thread.daemon = True  # ⚠️ DANGEROUS!
    thread.start()
```

**Problems:**
1. **Daemon threads killed without cleanup** on shutdown
2. **No concurrency limit** - can spawn unlimited threads
3. **No error propagation** - failures are silent
4. **No job tracking** - can't monitor or cancel
5. **Database connections held by threads** - pool exhaustion
6. **No retry logic** - transient failures permanent

**Impact:**
- Corrupted video records (status stuck in "processing")
- Database connection leaks
- Server crashes under high load
- Lost processing work
- No way to monitor job queue

**Recommended Solution: Celery + Redis**

**Installation:**
```bash
pip install celery[redis] redis
```

**Backend - Celery Setup:**
```python
# backend/app/celery_app.py
from celery import Celery

celery_app = Celery(
    'meteora',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
    worker_max_tasks_per_child=10,
)

# backend/app/tasks.py
from app.celery_app import celery_app
from app.services.video_processor import process_video

@celery_app.task(bind=True, max_retries=3)
def process_video_task(self, video_id: int):
    """Process video with retry logic"""
    try:
        return process_video(video_id)
    except Exception as exc:
        # Retry after 60 seconds
        raise self.retry(exc=exc, countdown=60)

# In upload_handler.py
def handle_upload_complete(file_path: str, metadata: dict):
    video = create_video_record(file_path, metadata)

    # Enqueue task instead of threading
    from app.tasks import process_video_task
    task = process_video_task.delay(video.id)

    logger.info(f"Queued processing job {task.id} for video {video.id}")
```

**Status Endpoint:**
```python
@router.get("/videos/{video_id}/processing-status")
async def get_processing_status(video_id: int):
    video = get_video(video_id)

    if video.celery_task_id:
        from celery.result import AsyncResult
        task = AsyncResult(video.celery_task_id)

        return {
            "status": task.state,
            "progress": task.info.get('progress', 0) if task.info else 0,
            "current": task.info.get('current', '') if task.info else '',
        }

    return {"status": video.status}
```

**Docker Compose:**
```yaml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery-worker:
    build: ./backend
    command: celery -A app.celery_app worker --loglevel=info --concurrency=2
    depends_on:
      - redis
      - db
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
```

**Acceptance Criteria:**
- [ ] Celery installed and configured
- [ ] Redis running in Docker Compose
- [ ] process_video converted to Celery task
- [ ] Retry logic implemented (max 3 retries)
- [ ] Job status queryable via API
- [ ] Worker concurrency limited (2-4 workers)
- [ ] Graceful shutdown handling
- [ ] Database sessions properly scoped
- [ ] Integration test with job queue

---

### Issue #5: [SECURITY] Docker Containers Running as Root

**Priority:** 🔴 Critical
**Type:** Security
**Effort:** 4 hours
**Component:** Docker Configuration

**Description:**
All Docker containers run as root user, violating principle of least privilege and increasing security risk.

**Affected Files:**
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `frontend/Dockerfile.dev`

**Security Impact:**
- Container escape = root access to host
- Compromised app = full container control
- File permission issues on volume mounts
- Fails security compliance audits

**Fix - Backend Dockerfile:**
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Install Python dependencies as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create videos directory and set ownership
RUN mkdir -p /app/videos && \
    chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Fix - Frontend Production Dockerfile:**
```dockerfile
# Build stage (can stay as root)
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Create non-root user for nginx
RUN addgroup -g 101 -S nginx && \
    adduser -S -D -H -u 101 -h /var/cache/nginx -s /sbin/nologin -G nginx -g nginx nginx

# Copy built assets
COPY --from=build --chown=nginx:nginx /app/dist /usr/share/nginx/html
COPY --chown=nginx:nginx nginx.conf /etc/nginx/conf.d/default.conf

# Adjust permissions
RUN chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# Switch to non-root user
USER nginx

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
```

**Nginx Config Adjustment:**
```nginx
# Change default port from 80 to 8080 (non-privileged)
server {
    listen 8080;
    # ... rest of config
}
```

**Docker Compose Port Update:**
```yaml
frontend-prod:
  ports:
    - "8080:8080"  # Update from 80:80
```

**Acceptance Criteria:**
- [ ] Backend runs as appuser (UID 1000)
- [ ] Frontend runs as nginx user
- [ ] All containers verified non-root: `docker exec <container> whoami`
- [ ] File permissions correct on volume mounts
- [ ] Services still function correctly
- [ ] Build process doesn't require root
- [ ] Security scan passes: `docker scan meteora-lx-backend`

**Testing:**
```bash
# Verify non-root
docker-compose up -d
docker exec meteora-lx-backend whoami  # Should output: appuser
docker exec meteora-lx-frontend whoami # Should output: nginx

# Verify permissions
docker exec meteora-lx-backend ls -la /app/videos
# Should show: drwxr-xr-x appuser appgroup
```

---

### Issue #6: [SECURITY] Hardcoded Passwords and Secrets in docker-compose.yml

**Priority:** 🔴 Critical
**Type:** Security
**Effort:** 1 hour
**Component:** Docker Configuration

**Description:**
Database password and connection strings are hardcoded in docker-compose.yml, visible in plain text.

**Affected File:**
`docker-compose.yml` lines 10-12, 33

**Current Code:**
```yaml
db:
  environment:
    POSTGRES_PASSWORD: meteora_password_change_in_production  # ❌ Plain text!

backend:
  environment:
    - DATABASE_URL=postgresql://meteora:meteora_password_change_in_production@db:5432/meteora_lx
```

**Security Impact:**
- Credentials visible in Git history
- Easy to accidentally commit
- No password rotation capability
- Fails security audits

**Recommended Fix - Use Docker Secrets:**

**Create secrets directory:**
```bash
mkdir -p secrets/
echo "$(openssl rand -base64 32)" > secrets/db_password.txt
echo "$(openssl rand -base64 32)" > secrets/jwt_secret.txt
chmod 600 secrets/*
```

**Update .gitignore:**
```gitignore
# Secrets
secrets/
*.secret
.env.production
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: meteora_lx
      POSTGRES_USER: meteora
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    # ... rest of config

  backend:
    build: ./backend
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password
      - JWT_SECRET_FILE=/run/secrets/jwt_secret
    secrets:
      - db_password
      - jwt_secret
    # ... rest of config

secrets:
  db_password:
    file: ./secrets/db_password.txt
  jwt_secret:
    file: ./secrets/jwt_secret.txt
```

**Backend - Read Secrets:**
```python
# backend/app/config.py
from pathlib import Path

class Settings(BaseSettings):
    DB_PASSWORD_FILE: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None

    @property
    def postgres_password(self) -> str:
        if self.DB_PASSWORD_FILE:
            return Path(self.DB_PASSWORD_FILE).read_text().strip()
        return self.POSTGRES_PASSWORD or "default_dev_password"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://meteora:{self.postgres_password}@db:5432/meteora_lx"
```

**Acceptance Criteria:**
- [ ] secrets/ directory created and gitignored
- [ ] Strong passwords generated (32+ chars)
- [ ] Docker secrets configured in compose file
- [ ] Backend reads secrets from files
- [ ] No plain text passwords in docker-compose.yml
- [ ] .env.example updated with instructions
- [ ] Documentation updated in README.Docker.md

**Production Note:**
For production, use external secrets management:
- AWS Secrets Manager
- HashiCorp Vault
- Kubernetes Secrets

---

## 🟠 HIGH PRIORITY (Complete Within 1 Week)

### Issue #7: [DEPENDENCIES] 36 Outdated Backend Packages

**Priority:** 🟠 High
**Type:** Maintenance, Security
**Effort:** 4-6 hours
**Component:** Backend Dependencies

**Description:**
Backend Python packages are significantly outdated, including security-critical packages like python-multipart.

**Affected File:**
`backend/requirements.txt`

**Critical Updates:**

| Package | Current | Latest | Gap | Risk |
|---------|---------|--------|-----|------|
| fastapi | 0.110.0 | 0.128.0 | 18 versions | Security patches |
| python-multipart | 0.0.9 | 0.0.21 | 12 versions | File upload security |
| sqlalchemy | 2.0.25 | 2.0.45 | 20 patches | Bug fixes |
| uvicorn | 0.27.0 | 0.40.0 | 13 versions | Performance |

**Recommendation:**
```bash
# Create backup
cp requirements.txt requirements.txt.backup

# Update packages
cat > requirements.txt << 'EOF'
fastapi==0.128.0
tuspyserver>=0.1.0
uvicorn[standard]==0.40.0
sqlalchemy==2.0.45
alembic==1.17.2
pydantic==2.12.5
pydantic-settings==2.12.0
python-multipart==0.0.21
aiofiles==25.1.0
python-dotenv==1.2.1
psycopg2-binary==2.9.11
EOF

# Install
pip install -r requirements.txt

# Test thoroughly
pytest
```

**Testing Checklist:**
- [ ] All unit tests pass
- [ ] Video upload works
- [ ] Video processing works
- [ ] Database queries work
- [ ] API endpoints respond correctly
- [ ] No deprecation warnings

**Acceptance Criteria:**
- [ ] All packages updated to latest stable
- [ ] requirements.txt committed
- [ ] CI/CD tests pass
- [ ] No breaking changes introduced
- [ ] Documentation updated if APIs changed

---

### Issue #8: [SECURITY] Add Security Headers to Nginx

**Priority:** 🟠 High
**Type:** Security
**Effort:** 1 hour
**Component:** Frontend - Nginx Configuration

**Description:**
Missing critical security headers: CSP, HSTS, Referrer-Policy, Permissions-Policy.

**Affected File:**
`frontend/nginx.conf`

**Current Headers:**
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
```

**Add Missing Headers:**
```nginx
server {
    listen 8080;
    root /usr/share/nginx/html;

    # Existing headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Content Security Policy
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self' http://backend:8000; media-src 'self' blob:; font-src 'self' data:; object-src 'none'; frame-ancestors 'self';" always;

    # HSTS (only if using HTTPS)
    # add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Referrer Policy
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Permissions Policy
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=(), usb=(), magnetometer=(), gyroscope=()" always;

    # ... rest of config
}
```

**Testing:**
```bash
# Test security headers
curl -I http://localhost:8080

# Or use online scanner
# https://securityheaders.com/
```

**Acceptance Criteria:**
- [ ] All headers added to nginx.conf
- [ ] CSP allows app to function correctly
- [ ] SecurityHeaders.com scan scores A or A+
- [ ] No console errors from CSP violations
- [ ] Documentation updated

---

### Issue #9: [PERFORMANCE] Consolidate Duplicate Frontend State Stores

**Priority:** 🟠 High
**Type:** Code Quality, Bug Risk
**Effort:** 4 hours
**Component:** Frontend - State Management

**Description:**
Two separate Zustand stores manage overlapping playback state, creating potential synchronization issues.

**Affected Files:**
- `frontend/src/stores/playerStore.ts` (103 LOC)
- `frontend/src/stores/timelineStore.ts` (187 LOC)

**Problem:**
```typescript
// playerStore.ts
interface PlayerState {
  isPlaying: boolean
  currentTime: number
  duration: number
  volume: number
  playbackRate: number
}

// timelineStore.ts (DUPLICATE!)
interface TimelineState {
  isPlaying: boolean
  currentTime: number
  duration: number
  volume: number
  playbackRate: number
  // ... plus timeline-specific state
}
```

**Impact:**
- State can become out of sync between player and timeline
- Duplicate code maintenance burden
- Confusing for developers
- Source of truth unclear

**Recommended Solution:**
```typescript
// frontend/src/stores/playbackStore.ts
interface PlaybackState {
  // Video reference
  videoId: number | null
  videoUrl: string | null

  // Playback state
  isPlaying: boolean
  currentTime: number
  duration: number
  volume: number
  playbackRate: number

  // Actions
  play: () => void
  pause: () => void
  togglePlay: () => void
  seek: (time: number) => void
  setVolume: (volume: number) => void
  setPlaybackRate: (rate: number) => void
}

// frontend/src/stores/timelineStore.ts (now just timeline-specific)
interface TimelineState {
  // Timeline display
  zoom: number
  panOffset: number
  showSceneNav: boolean
  hoveredTime: number | null

  // Data
  scenes: Scene[]
  keyframes: Keyframe[]

  // Actions
  setZoom: (zoom: number) => void
  nextScene: () => void
  previousScene: () => void
}

// Components use both stores
function VideoWorkspace() {
  const { isPlaying, currentTime, play, pause } = usePlaybackStore()
  const { scenes, zoom, nextScene } = useTimelineStore()
  // ...
}
```

**Migration Steps:**
1. Create new `playbackStore.ts` with consolidated state
2. Update VideoPlayer to use playbackStore
3. Update VideoWorkspace to use playbackStore + timelineStore
4. Update PlaybackControls to use playbackStore
5. Remove duplicate state from timelineStore
6. Delete playerStore.ts if no longer needed
7. Update tests

**Acceptance Criteria:**
- [ ] Single source of truth for playback state
- [ ] No state duplication
- [ ] All components updated
- [ ] Tests pass
- [ ] Video player and timeline synchronized
- [ ] No regression in functionality

---

### Issue #10: [SECURITY] Implement Rate Limiting on Upload Endpoints

**Priority:** 🟠 High
**Type:** Security, DoS Prevention
**Effort:** 2 hours
**Component:** Backend API

**Description:**
No rate limiting on upload or API endpoints, vulnerable to abuse and DoS attacks.

**Impact:**
- Unlimited uploads can exhaust storage
- API spam can exhaust resources
- No protection against abuse
- Hosting costs can spike

**Recommended Implementation:**

**Install slowapi:**
```bash
pip install slowapi
```

**Backend - Rate Limiter:**
```python
# backend/app/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Apply to endpoints
@app.post("/api/upload/")
@limiter.limit("10/hour")  # 10 uploads per hour per IP
async def upload_endpoint():
    ...

@app.get("/api/videos/")
@limiter.limit("100/minute")  # 100 requests per minute
async def list_videos():
    ...

# Health check excluded
@app.get("/api/health")
@limiter.exempt
async def health_check():
    ...
```

**Rate Limit Response:**
```json
{
  "error": "Rate limit exceeded",
  "detail": "10 per 1 hour",
  "retry_after": 3421
}
```

**Frontend - Handle Rate Limits:**
```typescript
async function uploadVideo(file: File) {
  try {
    const response = await fetch('/api/upload/', { ... })

    if (response.status === 429) {
      const retryAfter = response.headers.get('Retry-After')
      toast({
        title: "Rate limit exceeded",
        description: `Please try again in ${retryAfter} seconds`
      })
      return
    }
    // ... normal flow
  } catch (error) {
    // ...
  }
}
```

**Configuration:**
```python
# Different limits for authenticated users
RATE_LIMITS = {
    "upload": {
        "anonymous": "5/hour",
        "authenticated": "50/hour",
        "premium": "unlimited"
    },
    "api": {
        "anonymous": "50/minute",
        "authenticated": "500/minute"
    }
}
```

**Acceptance Criteria:**
- [ ] slowapi installed and configured
- [ ] Upload endpoint limited (10/hour for now)
- [ ] API endpoints limited (100/min)
- [ ] Health check exempt from limits
- [ ] 429 responses include Retry-After header
- [ ] Frontend handles rate limit errors gracefully
- [ ] Documentation updated with limits
- [ ] Consider Redis for distributed rate limiting

---

### Issue #11: [BUG] Fix ESLint Errors in Frontend

**Priority:** 🟠 High
**Type:** Code Quality
**Effort:** 2 hours
**Component:** Frontend

**Description:**
4 ESLint errors preventing clean builds and violating React best practices.

**Errors:**

**1. Fast Refresh Export Violations**
```typescript
// ❌ button.tsx, badge.tsx
export { Button, buttonVariants }
// Mixing component and non-component exports breaks Fast Refresh
```

**Fix:**
```typescript
// components/ui/button.tsx - Export component only
export { Button }

// NEW: lib/button-variants.ts - Export variants separately
import { cva } from "class-variance-authority"

export const buttonVariants = cva(
  "inline-flex items-center...",
  { variants: { ... } }
)

// Update imports elsewhere
import { Button } from "@/components/ui/button"
import { buttonVariants } from "@/lib/button-variants"
```

**2. setState in useEffect**
```typescript
// ❌ VideoWorkspace.tsx line 36
useEffect(() => {
  setIsLoading(true)  // Anti-pattern
  Promise.all([...]).then(...)
}, [videoId])
```

**Fix:**
```typescript
// Use derived state or move outside effect
const [loadingStates, setLoadingStates] = useState({
  metadata: false,
  scenes: false,
  keyframes: false
})

useEffect(() => {
  const load = async () => {
    setLoadingStates(prev => ({ ...prev, metadata: true }))
    const metadata = await fetch(...)
    setLoadingStates(prev => ({ ...prev, metadata: false, scenes: true }))
    // ...
  }
  load()
}, [videoId])
```

**3. Unused Type-Only Variable**
```typescript
// ❌ use-toast.ts line 15
const actionTypes = {  // Used only as a type
  ADD_TOAST: "ADD_TOAST",
} as const
```

**Fix:**
```typescript
type ActionTypes = {
  ADD_TOAST: "ADD_TOAST"
  // ...
} as const

// Or use satisfies
const actionTypes = {
  ADD_TOAST: "ADD_TOAST"
} as const satisfies Record<string, string>
```

**Acceptance Criteria:**
- [ ] All 4 ESLint errors fixed
- [ ] npm run build succeeds with 0 errors
- [ ] Fast Refresh working correctly
- [ ] No new ESLint errors introduced
- [ ] Code still functions as expected

---

### Issue #12: [PERFORMANCE] Add Database Indexes for Common Queries

**Priority:** 🟠 High
**Type:** Performance
**Effort:** 2 hours
**Component:** Backend - Database

**Description:**
Missing indexes on frequently queried fields will cause slow queries as data grows.

**Affected File:**
`backend/app/models/video.py`

**Current Indexes:**
- `videos.id` (primary key, auto-indexed)
- `videos.filename` (line 10)
- `videos.file_path` (unique, auto-indexed)

**Missing Indexes:**
```sql
-- Videos filtered by status
SELECT * FROM videos WHERE status = 'completed';
-- No index! Will be slow with 10k+ videos

-- Videos sorted by upload date
SELECT * FROM videos ORDER BY uploaded_at DESC LIMIT 10;
-- No index! Sequential scan

-- Scenes for a video
SELECT * FROM scenes WHERE video_id = 5;
-- Foreign key but no explicit index!
```

**Add Missing Indexes:**
```python
# backend/app/models/video.py

from sqlalchemy import Index

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_path = Column(String, unique=True)
    status = Column(String, default="uploaded", index=True)  # ← ADD INDEX
    uploaded_at = Column(DateTime, default=datetime.utcnow, index=True)  # ← ADD INDEX
    # ...

    # Composite index for common query
    __table_args__ = (
        Index('ix_video_status_uploaded', 'status', 'uploaded_at'),
    )

class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), index=True)  # ← ADD INDEX
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    importance_score = Column(Float, default=0.5)

    # Index for finding scenes by time
    __table_args__ = (
        Index('ix_scene_video_time', 'video_id', 'start_time'),
    )

class Keyframe(Base):
    __tablename__ = "keyframes"

    id = Column(Integer, primary_key=True, index=True)
    scene_id = Column(Integer, ForeignKey("scenes.id"), index=True)  # ← ADD INDEX
    video_id = Column(Integer, index=True)  # ← ADD INDEX for direct queries
    timestamp = Column(Float, nullable=False)
    importance_score = Column(Float, default=0.5)
```

**Create Migration:**
```bash
alembic revision -m "Add performance indexes"
```

**Migration File:**
```python
def upgrade():
    op.create_index('ix_videos_status', 'videos', ['status'])
    op.create_index('ix_videos_uploaded_at', 'videos', ['uploaded_at'])
    op.create_index('ix_video_status_uploaded', 'videos', ['status', 'uploaded_at'])
    op.create_index('ix_scenes_video_id', 'scenes', ['video_id'])
    op.create_index('ix_scene_video_time', 'scenes', ['video_id', 'start_time'])
    op.create_index('ix_keyframes_scene_id', 'keyframes', ['scene_id'])
    op.create_index('ix_keyframes_video_id', 'keyframes', ['video_id'])

def downgrade():
    op.drop_index('ix_keyframes_video_id')
    op.drop_index('ix_keyframes_scene_id')
    op.drop_index('ix_scene_video_time')
    op.drop_index('ix_scenes_video_id')
    op.drop_index('ix_video_status_uploaded')
    op.drop_index('ix_videos_uploaded_at')
    op.drop_index('ix_videos_status')
```

**Verify Performance:**
```sql
-- Before: Sequential scan
EXPLAIN SELECT * FROM videos WHERE status = 'completed';

-- After: Index scan
EXPLAIN SELECT * FROM videos WHERE status = 'completed';
-- Should show "Index Scan using ix_videos_status"
```

**Acceptance Criteria:**
- [ ] Indexes added to models
- [ ] Alembic migration created
- [ ] Migration tested locally
- [ ] EXPLAIN shows index usage
- [ ] No performance regression
- [ ] Documentation updated

---

### Issue #13: [SECURITY] Add File Content Validation (Magic Bytes)

**Priority:** 🟠 High
**Type:** Security
**Effort:** 2-3 hours
**Component:** Backend - Upload Validation

**Description:**
Currently only validates MIME type from client metadata. Malicious users can upload any file disguised as video.

**Current Validation:**
```python
# Client-side only
if (!file.type.startsWith('video/')) {
  // Reject
}

# Server-side: Trusts client metadata
mime_type = metadata.get('filetype', 'video/mp4')  # ❌ Unsafe!
```

**Security Risk:**
- Malware disguised as .mp4
- Executable files uploaded
- Storage of harmful content
- Serving malicious files to users

**Recommended Implementation:**

**Install python-magic:**
```bash
pip install python-magic
```

**Backend - File Validation:**
```python
# backend/app/services/file_validator.py
import magic
from pathlib import Path

ALLOWED_VIDEO_MIMES = [
    'video/mp4',
    'video/mpeg',
    'video/quicktime',
    'video/x-msvideo',
    'video/x-matroska',
    'video/webm'
]

def validate_video_file(file_path: str) -> dict:
    """
    Validate that uploaded file is actually a video.

    Returns:
        {"valid": bool, "mime_type": str, "error": str}
    """
    try:
        # Check file exists
        path = Path(file_path)
        if not path.exists():
            return {"valid": False, "error": "File not found"}

        # Check magic bytes (first 2048 bytes)
        mime = magic.Magic(mime=True)
        detected_mime = mime.from_file(file_path)

        # Verify it's a video
        if not detected_mime.startswith('video/'):
            return {
                "valid": False,
                "mime_type": detected_mime,
                "error": f"File is not a video: {detected_mime}"
            }

        # Verify it's an allowed video type
        if detected_mime not in ALLOWED_VIDEO_MIMES:
            return {
                "valid": False,
                "mime_type": detected_mime,
                "error": f"Unsupported video format: {detected_mime}"
            }

        # Double-check with ffprobe
        import subprocess
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_format', '-show_streams', file_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return {
                "valid": False,
                "error": "File is not a valid video (ffprobe check failed)"
            }

        return {
            "valid": True,
            "mime_type": detected_mime,
            "error": None
        }

    except Exception as e:
        return {"valid": False, "error": f"Validation error: {str(e)}"}

# In upload_handler.py
from app.services.file_validator import validate_video_file

def handle_upload_complete(file_path: str, metadata: dict):
    # Validate file before processing
    validation = validate_video_file(file_path)

    if not validation["valid"]:
        logger.error(f"Invalid file upload: {validation['error']}")
        # Delete malicious file
        os.remove(file_path)
        raise ValueError(f"Invalid video file: {validation['error']}")

    # Use detected MIME type, not client-provided
    mime_type = validation["mime_type"]

    # Create video record with validated MIME
    video = Video(
        filename=secure_filename(metadata.get('filename')),
        file_path=file_path,
        mime_type=mime_type,  # ← Use validated type
        # ...
    )
    # ...
```

**Testing:**
```python
def test_rejects_malicious_file():
    # Create fake video (actually a text file)
    fake_video = Path("/tmp/malware.mp4")
    fake_video.write_text("echo 'malware'")

    validation = validate_video_file(str(fake_video))

    assert validation["valid"] is False
    assert "not a video" in validation["error"]

def test_accepts_real_video():
    validation = validate_video_file("tests/fixtures/sample.mp4")

    assert validation["valid"] is True
    assert validation["mime_type"] == "video/mp4"
```

**Acceptance Criteria:**
- [ ] python-magic installed
- [ ] validate_video_file() implemented
- [ ] Called in upload_handler before processing
- [ ] Malicious files rejected and deleted
- [ ] Detected MIME type used (not client-provided)
- [ ] ffprobe double-check implemented
- [ ] Unit tests for validation
- [ ] Error handling and logging
- [ ] Documentation updated

---

### Issue #14: [FRONTEND] Create Centralized API Client

**Priority:** 🟠 High
**Type:** Code Quality, Maintainability
**Effort:** 3 hours
**Component:** Frontend - API Integration

**Description:**
API calls scattered throughout codebase with hardcoded URLs and inconsistent error handling.

**Current Issues:**
- 7 instances of `http://localhost:8000` hardcoded
- No centralized error handling
- No request/response interceptors
- No retry logic
- Can't add auth tokens globally

**Affected Files:**
- `frontend/src/stores/videoStore.ts` (lines 85, 100, 115, 130)
- `frontend/src/components/workspace/VideoWorkspace.tsx` (lines 40-42)

**Recommended Implementation:**

**Create API Client:**
```typescript
// frontend/src/lib/api.ts
import { authStore } from '@/stores/authStore'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: any
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

interface RequestOptions extends RequestInit {
  timeout?: number
  retry?: number
}

async function request<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { timeout = 30000, retry = 0, ...fetchOptions } = options

  // Add authentication
  const token = authStore.getState().token
  const headers = new Headers(fetchOptions.headers)
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }
  headers.set('Content-Type', 'application/json')

  // Create abort controller for timeout
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), timeout)

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...fetchOptions,
      headers,
      signal: controller.signal,
    })

    clearTimeout(timeoutId)

    // Handle non-OK responses
    if (!response.ok) {
      const error = await response.json().catch(() => ({}))

      // Handle rate limiting
      if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After')
        throw new ApiError(
          `Rate limit exceeded. Retry after ${retryAfter}s`,
          429,
          { retryAfter: parseInt(retryAfter || '60') }
        )
      }

      // Handle auth errors
      if (response.status === 401) {
        authStore.getState().logout()
        throw new ApiError('Unauthorized', 401)
      }

      throw new ApiError(
        error.detail || `Request failed: ${response.statusText}`,
        response.status,
        error
      )
    }

    // Parse response
    const contentType = response.headers.get('content-type')
    if (contentType?.includes('application/json')) {
      return response.json()
    }

    return response.text() as any

  } catch (error) {
    clearTimeout(timeoutId)

    // Retry logic
    if (retry > 0 && error instanceof ApiError && error.status >= 500) {
      console.log(`Retrying request (${retry} attempts left)...`)
      await new Promise(resolve => setTimeout(resolve, 1000))
      return request<T>(endpoint, { ...options, retry: retry - 1 })
    }

    // Timeout error
    if (error.name === 'AbortError') {
      throw new ApiError('Request timeout', 408)
    }

    throw error
  }
}

// Convenience methods
export const api = {
  get: <T>(endpoint: string, options?: RequestOptions) =>
    request<T>(endpoint, { ...options, method: 'GET' }),

  post: <T>(endpoint: string, data?: any, options?: RequestOptions) =>
    request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: JSON.stringify(data),
    }),

  put: <T>(endpoint: string, data?: any, options?: RequestOptions) =>
    request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  delete: <T>(endpoint: string, options?: RequestOptions) =>
    request<T>(endpoint, { ...options, method: 'DELETE' }),
}

// Type-safe API methods
export const videoApi = {
  list: (skip = 0, limit = 100) =>
    api.get<{ videos: Video[] }>(`/videos?skip=${skip}&limit=${limit}`),

  get: (id: number) =>
    api.get<Video>(`/videos/${id}`),

  getStatus: (id: number) =>
    api.get<VideoStatus>(`/videos/${id}/status`),

  getScenes: (id: number) =>
    api.get<{ scenes: Scene[] }>(`/videos/${id}/scenes`),

  getKeyframes: (id: number) =>
    api.get<{ keyframes: Keyframe[] }>(`/videos/${id}/keyframes`),
}
```

**Usage:**
```typescript
// Before (scattered, inconsistent)
const response = await fetch('http://localhost:8000/api/videos/1')
const video = await response.json()

// After (centralized, type-safe)
import { videoApi } from '@/lib/api'

const video = await videoApi.get(1)
// Type-safe, automatic error handling, auth tokens added
```

**Error Handling:**
```typescript
import { ApiError } from '@/lib/api'

try {
  const videos = await videoApi.list()
} catch (error) {
  if (error instanceof ApiError) {
    if (error.status === 429) {
      toast({ title: "Rate limited", description: error.message })
    } else if (error.status === 401) {
      toast({ title: "Please log in" })
    } else {
      toast({ title: "Error", description: error.message })
    }
  }
}
```

**Environment Configuration:**
```env
# .env.development
VITE_API_URL=http://localhost:8000/api

# .env.production
VITE_API_URL=https://api.meteora-lx.com/api
```

**Acceptance Criteria:**
- [ ] api.ts created with request() function
- [ ] GET, POST, PUT, DELETE methods
- [ ] Authentication token injection
- [ ] Error handling and retry logic
- [ ] Timeout support
- [ ] Type-safe video API methods
- [ ] All 7 fetch() calls refactored to use api client
- [ ] Environment-based URL configuration
- [ ] Documentation with usage examples

---

### Issue #15: [DOCKER] Remove Database Port Exposure in Production

**Priority:** 🟠 High
**Type:** Security
**Effort:** 30 minutes
**Component:** Docker Configuration

**Description:**
PostgreSQL port 5432 is exposed to host network, allowing potential unauthorized access.

**Affected File:**
`docker-compose.yml` lines 15-16

**Current Configuration:**
```yaml
db:
  image: postgres:16-alpine
  ports:
    - "5432:5432"  # ❌ Exposed to host!
```

**Security Risk:**
- Database accessible from host network
- Potential brute-force attacks
- Data exfiltration if password compromised
- Should only be accessible within Docker network

**Fix:**
```yaml
# docker-compose.yml (development - keep for debugging)
db:
  ports:
    - "5432:5432"  # OK for development

# docker-compose.prod.yml (production - no exposure)
db:
  # Remove ports entirely
  # Only backend can access via Docker network
  expose:
    - "5432"  # Internal only
```

**Or use conditional port mapping:**
```yaml
db:
  ports:
    # Only expose in development
    ${DB_EXPOSE_PORT:-}  # Empty in prod, "5432:5432" in dev
```

**.env.development:**
```env
DB_EXPOSE_PORT=5432:5432
```

**.env.production:**
```env
DB_EXPOSE_PORT=  # Empty = no exposure
```

**Verification:**
```bash
# Production should not show 5432
docker-compose -f docker-compose.prod.yml ps

# Should only show 8080 (frontend), not 5432
```

**Acceptance Criteria:**
- [ ] Database port not exposed in production
- [ ] Backend can still connect via Docker network
- [ ] Development can still expose for debugging (optional)
- [ ] Documentation updated
- [ ] Verified with `docker-compose ps`

---

## 📝 Summary

**Total Issues Created:** 15

**Breakdown:**
- 🔴 **Critical:** 6 issues (24-30 hours)
- 🟠 **High:** 9 issues (25-31 hours)
- **Total Effort:** 49-61 hours (~1.5-2 weeks)

**Priority Order:**
1. Path traversal vulnerability (30 min)
2. Hardcoded secrets (1 hr)
3. Broken video processing (2 hrs)
4. Docker root user (4 hrs)
5. Authentication system (8-12 hrs)
6. Daemon thread → Celery (8 hrs)
7. Update dependencies (4-6 hrs)
8. Rate limiting (2 hrs)
9. Security headers (1 hr)
10. File validation (2-3 hrs)
11. Database indexes (2 hrs)
12. Consolidate stores (4 hrs)
13. Fix ESLint errors (2 hrs)
14. API client (3 hrs)
15. Database port (30 min)

---

**Next Steps:**
1. Copy these issues to GitHub
2. Assign to team members
3. Create milestone "Production Readiness"
4. Set up project board
5. Begin with Critical items

Would you like me to:
- Format these as actual GitHub issue templates?
- Create a project board structure?
- Prioritize differently?
