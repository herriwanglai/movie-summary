# 🎬 Video Upload & Import Workflow

## Overview

Complete workflow for importing movies into the analysis system with:
- Multiple upload methods (local file, URL, cloud storage)
- Chunked upload for large files
- Real-time progress tracking
- Automatic analysis pipeline trigger
- Video library management

---

## 🎯 Upload Methods

### 1. **Local File Upload** (Primary Method)

```
┌─────────────────────────────────────────────────┐
│ 🎬 Movie Analysis Studio                        │
├─────────────────────────────────────────────────┤
│                                                 │
│         No videos uploaded yet                  │
│                                                 │
│   ┌───────────────────────────────────────┐    │
│   │                                       │    │
│   │        📁 Drop video file here        │    │
│   │              or                       │    │
│   │      [📤 Choose File from Computer]   │    │
│   │                                       │    │
│   │  Supported: MP4, MKV, AVI, MOV        │    │
│   │  Max size: 10 GB                      │    │
│   │                                       │    │
│   └───────────────────────────────────────┘    │
│                                                 │
│   Other options:                                │
│   [🌐 Import from URL]                          │
│   [☁️ Import from Cloud Storage]                │
│   [📂 Browse Sample Videos]                     │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 2. **URL Import**

```
┌─────────────────────────────────────────────────┐
│ Import from URL                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│ Video URL:                                      │
│ ┌─────────────────────────────────────────────┐ │
│ │ https://example.com/movie.mp4               │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ ☑️ Download to server                           │
│ ☐ Stream directly (experimental)               │
│                                                 │
│ [Cancel] [Import Video]                        │
└─────────────────────────────────────────────────┘
```

### 3. **Cloud Storage Import**

```
┌─────────────────────────────────────────────────┐
│ Import from Cloud Storage                       │
├─────────────────────────────────────────────────┤
│                                                 │
│ Select Source:                                  │
│ [Google Drive] [Dropbox] [OneDrive] [S3]       │
│                                                 │
│ ┌─────────────────────────────────────────────┐ │
│ │ 📁 My Videos/                               │ │
│ │   ├─ 📹 movie1.mp4 (2.5 GB)                │ │
│ │   ├─ 📹 movie2.mkv (4.2 GB)                │ │
│ │   └─ 📹 documentary.avi (1.8 GB)           │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ Selected: movie1.mp4                            │
│                                                 │
│ [Cancel] [Import Selected]                     │
└─────────────────────────────────────────────────┘
```

---

## 📤 Upload Process Flow

### Step-by-Step Workflow

```
┌─────────────────────────────────────────────────┐
│ Step 1: User Selects Video                      │
│ - Drag & drop file                              │
│ - Click "Choose File"                           │
│ - Paste URL                                     │
│ - Select from cloud                             │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ Step 2: File Validation                         │
│ ✓ Check file format (MP4/MKV/AVI/MOV/WebM)     │
│ ✓ Check file size (< 10 GB)                    │
│ ✓ Verify video codec                           │
│ ✓ Check if already uploaded (hash check)       │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ Step 3: Upload Preparation                      │
│ - Generate unique video ID                      │
│ - Create upload session                         │
│ - Calculate chunks (for large files)            │
│ - Initialize progress tracking                  │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ Step 4: Chunked Upload                          │
│ ┌─────────────────────────────────────────────┐ │
│ │ Uploading: movie.mp4                        │ │
│ │ ████████████░░░░░░░░░░░ 65%                │ │
│ │ 1.3 GB / 2.0 GB                             │ │
│ │ Speed: 5.2 MB/s • ETA: 2m 15s               │ │
│ │                                             │ │
│ │ Chunk 13/20 uploading...                    │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ [⏸️ Pause] [❌ Cancel]                          │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ Step 5: Processing                              │
│ ✓ Upload complete!                              │
│ 🔄 Processing video...                          │
│                                                 │
│ Current tasks:                                  │
│ ✓ Verifying file integrity                     │
│ ✓ Extracting metadata                          │
│ 🔄 Generating preview thumbnail                │
│ ⏳ Starting scene detection                     │
│ ⏳ Extracting audio                             │
│                                                 │
│ This may take a few minutes...                  │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ Step 6: Analysis Options                        │
│ Video uploaded successfully! ✅                  │
│                                                 │
│ Choose analysis level:                          │
│ ○ Quick Preview (1-2 min)                      │
│   - Basic scene detection                      │
│   - Keyframe extraction                        │
│                                                 │
│ ● Standard Analysis (5-10 min)                 │
│   - Scene detection                            │
│   - Transcription                              │
│   - Importance analysis                        │
│   - Character detection                        │
│                                                 │
│ ○ Deep Analysis (15-30 min)                    │
│   - Everything in Standard                     │
│   - AI summary generation                      │
│   - Theme identification                       │
│   - Character relationship mapping             │
│                                                 │
│ [Start Analysis] [Skip for Now]                │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ Step 7: Analysis in Progress                    │
│ Analyzing: movie.mp4                            │
│                                                 │
│ ✓ Scene detection (50 scenes found)            │
│ ✓ Keyframe extraction (150 frames)             │
│ 🔄 Transcribing audio... 45%                    │
│ ⏳ Importance analysis                          │
│ ⏳ AI summary generation                        │
│                                                 │
│ ████████░░░░░░░░ 55%                           │
│ Estimated time: 3 minutes remaining             │
│                                                 │
│ [View Progress Details] [Cancel Analysis]      │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ Step 8: Analysis Complete!                      │
│ ✅ Analysis complete!                           │
│                                                 │
│ Results:                                        │
│ • 50 scenes detected                            │
│ • 150 keyframes extracted                       │
│ • 2,345 words transcribed                       │
│ • 12 important moments identified               │
│ • 5 main characters detected                    │
│                                                 │
│ [🎬 Start Analyzing] [📊 View Summary]          │
└─────────────────────────────────────────────────┘
```

---

## 🎨 Upload UI Components

### 1. Drag & Drop Zone

```tsx
// components/UploadZone/UploadZone.tsx
interface UploadZoneProps {
  onFileSelect: (file: File) => void;
  maxSize?: number;
  acceptedFormats?: string[];
}

export const UploadZone: React.FC<UploadZoneProps> = ({
  onFileSelect,
  maxSize = 10 * 1024 * 1024 * 1024, // 10 GB
  acceptedFormats = ['.mp4', '.mkv', '.avi', '.mov', '.webm']
}) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    const videoFile = files.find(file =>
      acceptedFormats.some(format =>
        file.name.toLowerCase().endsWith(format)
      )
    );

    if (videoFile) {
      validateAndUpload(videoFile);
    } else {
      toast.error('Please drop a valid video file');
    }
  };

  const validateAndUpload = async (file: File) => {
    // Validate file size
    if (file.size > maxSize) {
      toast.error(`File too large. Max size: ${formatBytes(maxSize)}`);
      return;
    }

    // Validate format
    if (!acceptedFormats.some(fmt => file.name.toLowerCase().endsWith(fmt))) {
      toast.error('Unsupported file format');
      return;
    }

    // Check if already uploaded (using file hash)
    const fileHash = await calculateFileHash(file);
    const existing = await checkExistingVideo(fileHash);

    if (existing) {
      const confirm = await showConfirm(
        'This video has already been uploaded. Upload again?'
      );
      if (!confirm) return;
    }

    onFileSelect(file);
  };

  return (
    <div
      className={`upload-zone ${isDragging ? 'dragging' : ''}`}
      onDrop={handleDrop}
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
    >
      <div className="upload-icon">
        <FileUploadIcon size={64} />
      </div>

      <h3>Drop video file here</h3>
      <p>or</p>

      <input
        type="file"
        id="file-input"
        accept={acceptedFormats.join(',')}
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) validateAndUpload(file);
        }}
        style={{ display: 'none' }}
      />

      <label htmlFor="file-input" className="upload-button">
        📤 Choose File from Computer
      </label>

      <div className="upload-info">
        <p>Supported formats: {acceptedFormats.join(', ')}</p>
        <p>Maximum size: {formatBytes(maxSize)}</p>
      </div>
    </div>
  );
};
```

### 2. Upload Progress Component

```tsx
// components/UploadProgress/UploadProgress.tsx
interface UploadProgressProps {
  file: File;
  progress: number;
  uploadedBytes: number;
  totalBytes: number;
  speed: number; // bytes per second
  status: 'uploading' | 'paused' | 'processing' | 'complete' | 'error';
  onPause: () => void;
  onResume: () => void;
  onCancel: () => void;
}

export const UploadProgress: React.FC<UploadProgressProps> = ({
  file,
  progress,
  uploadedBytes,
  totalBytes,
  speed,
  status,
  onPause,
  onResume,
  onCancel
}) => {
  const eta = speed > 0 ? (totalBytes - uploadedBytes) / speed : 0;

  return (
    <div className="upload-progress-card">
      <div className="file-info">
        <FileVideoIcon size={40} />
        <div className="file-details">
          <h4>{file.name}</h4>
          <p className="file-size">
            {formatBytes(uploadedBytes)} / {formatBytes(totalBytes)}
          </p>
        </div>
      </div>

      <div className="progress-bar-container">
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${progress}%` }}
          />
        </div>
        <span className="progress-text">{progress}%</span>
      </div>

      <div className="upload-stats">
        <div className="stat">
          <span className="label">Speed:</span>
          <span className="value">{formatSpeed(speed)}</span>
        </div>
        <div className="stat">
          <span className="label">ETA:</span>
          <span className="value">{formatDuration(eta)}</span>
        </div>
        <div className="stat">
          <span className="label">Status:</span>
          <span className={`status status-${status}`}>
            {status === 'uploading' && '🔄 Uploading'}
            {status === 'paused' && '⏸️ Paused'}
            {status === 'processing' && '⚙️ Processing'}
            {status === 'complete' && '✅ Complete'}
            {status === 'error' && '❌ Error'}
          </span>
        </div>
      </div>

      <div className="upload-actions">
        {status === 'uploading' && (
          <button onClick={onPause} className="btn-pause">
            ⏸️ Pause
          </button>
        )}
        {status === 'paused' && (
          <button onClick={onResume} className="btn-resume">
            ▶️ Resume
          </button>
        )}
        {status !== 'complete' && (
          <button onClick={onCancel} className="btn-cancel">
            ❌ Cancel
          </button>
        )}
      </div>
    </div>
  );
};
```

### 3. Video Library Component

```tsx
// components/VideoLibrary/VideoLibrary.tsx
interface VideoLibraryProps {
  videos: Video[];
  onVideoSelect: (video: Video) => void;
  onVideoDelete: (videoId: string) => void;
}

export const VideoLibrary: React.FC<VideoLibraryProps> = ({
  videos,
  onVideoSelect,
  onVideoDelete
}) => {
  const [sortBy, setSortBy] = useState<'date' | 'name' | 'duration'>('date');
  const [filterStatus, setFilterStatus] = useState<'all' | 'analyzed' | 'pending'>('all');

  const filteredVideos = videos
    .filter(v => {
      if (filterStatus === 'all') return true;
      if (filterStatus === 'analyzed') return v.analyzed;
      if (filterStatus === 'pending') return !v.analyzed;
      return true;
    })
    .sort((a, b) => {
      if (sortBy === 'date') return b.uploadedAt - a.uploadedAt;
      if (sortBy === 'name') return a.filename.localeCompare(b.filename);
      if (sortBy === 'duration') return b.duration - a.duration;
      return 0;
    });

  return (
    <div className="video-library">
      <div className="library-header">
        <h2>Video Library ({videos.length})</h2>

        <div className="library-controls">
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
            <option value="date">Sort by Date</option>
            <option value="name">Sort by Name</option>
            <option value="duration">Sort by Duration</option>
          </select>

          <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
            <option value="all">All Videos</option>
            <option value="analyzed">Analyzed</option>
            <option value="pending">Pending Analysis</option>
          </select>
        </div>
      </div>

      <div className="video-grid">
        {filteredVideos.map(video => (
          <VideoCard
            key={video.id}
            video={video}
            onClick={() => onVideoSelect(video)}
            onDelete={() => onVideoDelete(video.id)}
          />
        ))}
      </div>
    </div>
  );
};

const VideoCard: React.FC<{
  video: Video;
  onClick: () => void;
  onDelete: () => void;
}> = ({ video, onClick, onDelete }) => {
  return (
    <div className="video-card" onClick={onClick}>
      <div className="video-thumbnail">
        <img src={video.thumbnailUrl} alt={video.filename} />
        {!video.analyzed && (
          <div className="pending-badge">⏳ Pending Analysis</div>
        )}
        {video.analyzed && (
          <div className="analyzed-badge">✅ Analyzed</div>
        )}
      </div>

      <div className="video-info">
        <h4 className="video-title">{video.filename}</h4>
        <div className="video-meta">
          <span>{formatDuration(video.duration)}</span>
          <span>•</span>
          <span>{formatBytes(video.fileSize)}</span>
          <span>•</span>
          <span>{formatDate(video.uploadedAt)}</span>
        </div>

        {video.analyzed && (
          <div className="video-stats">
            <span>📊 {video.sceneCount} scenes</span>
            <span>📸 {video.screenshotCount} screenshots</span>
            <span>✂️ {video.clipCount} clips</span>
          </div>
        )}
      </div>

      <div className="video-actions" onClick={(e) => e.stopPropagation()}>
        <button onClick={() => onClick()} title="Open">
          🎬 Open
        </button>
        <button onClick={onDelete} className="delete-btn" title="Delete">
          🗑️
        </button>
      </div>
    </div>
  );
};
```

---

## 🔧 Backend Upload Service

### 1. Chunked Upload API

```python
# api/upload.py
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import hashlib
import os

router = APIRouter()

# Configuration
UPLOAD_DIR = "./uploads"
CHUNK_SIZE = 5 * 1024 * 1024  # 5 MB chunks
MAX_FILE_SIZE = 10 * 1024 * 1024 * 1024  # 10 GB

@router.post("/api/upload/initialize")
async def initialize_upload(
    filename: str = Form(...),
    file_size: int = Form(...),
    file_hash: str = Form(...)
):
    """Initialize upload session"""

    # Check if file already exists
    existing = await check_existing_video(file_hash)
    if existing:
        return {"exists": True, "video_id": existing.id}

    # Validate file size
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large")

    # Create upload session
    upload_id = generate_upload_id()
    session = {
        "upload_id": upload_id,
        "filename": filename,
        "file_size": file_size,
        "file_hash": file_hash,
        "chunks_uploaded": [],
        "created_at": datetime.now()
    }

    # Save session
    await save_upload_session(session)

    # Create upload directory
    upload_path = os.path.join(UPLOAD_DIR, upload_id)
    os.makedirs(upload_path, exist_ok=True)

    return {
        "upload_id": upload_id,
        "chunk_size": CHUNK_SIZE,
        "total_chunks": (file_size + CHUNK_SIZE - 1) // CHUNK_SIZE
    }


@router.post("/api/upload/chunk")
async def upload_chunk(
    upload_id: str = Form(...),
    chunk_index: int = Form(...),
    chunk: UploadFile = File(...)
):
    """Upload a single chunk"""

    # Get upload session
    session = await get_upload_session(upload_id)
    if not session:
        raise HTTPException(404, "Upload session not found")

    # Save chunk
    chunk_path = os.path.join(UPLOAD_DIR, upload_id, f"chunk_{chunk_index}")
    with open(chunk_path, "wb") as f:
        content = await chunk.read()
        f.write(content)

    # Update session
    session["chunks_uploaded"].append(chunk_index)
    await save_upload_session(session)

    # Calculate progress
    total_chunks = (session["file_size"] + CHUNK_SIZE - 1) // CHUNK_SIZE
    progress = len(session["chunks_uploaded"]) / total_chunks * 100

    return {
        "chunk_index": chunk_index,
        "progress": progress,
        "chunks_remaining": total_chunks - len(session["chunks_uploaded"])
    }


@router.post("/api/upload/complete")
async def complete_upload(upload_id: str = Form(...)):
    """Finalize upload and merge chunks"""

    session = await get_upload_session(upload_id)
    if not session:
        raise HTTPException(404, "Upload session not found")

    # Merge chunks
    output_path = os.path.join(UPLOAD_DIR, f"{upload_id}.mp4")
    total_chunks = (session["file_size"] + CHUNK_SIZE - 1) // CHUNK_SIZE

    with open(output_path, "wb") as outfile:
        for i in range(total_chunks):
            chunk_path = os.path.join(UPLOAD_DIR, upload_id, f"chunk_{i}")
            with open(chunk_path, "rb") as infile:
                outfile.write(infile.read())

    # Verify file integrity
    file_hash = calculate_file_hash(output_path)
    if file_hash != session["file_hash"]:
        os.remove(output_path)
        raise HTTPException(400, "File integrity check failed")

    # Create video record
    video = await create_video_record({
        "filename": session["filename"],
        "path": output_path,
        "file_size": session["file_size"],
        "file_hash": file_hash,
        "uploaded_at": datetime.now(),
        "analyzed": False
    })

    # Clean up chunks
    import shutil
    shutil.rmtree(os.path.join(UPLOAD_DIR, upload_id))

    # Trigger analysis (optional)
    if auto_analyze:
        await trigger_analysis(video.id)

    return {
        "video_id": video.id,
        "status": "upload_complete"
    }


@router.post("/api/upload/from-url")
async def upload_from_url(url: str = Form(...)):
    """Download video from URL"""

    # Validate URL
    if not is_valid_video_url(url):
        raise HTTPException(400, "Invalid video URL")

    # Start download in background
    task_id = await start_download_task(url)

    return {
        "task_id": task_id,
        "status": "downloading"
    }


@router.get("/api/upload/status/{task_id}")
async def get_upload_status(task_id: str):
    """Get upload/download status"""

    task = await get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    return {
        "status": task.status,
        "progress": task.progress,
        "video_id": task.video_id if task.status == "complete" else None
    }
```

### 2. Analysis Trigger

```python
# services/analysis_service.py
async def trigger_analysis(
    video_id: str,
    level: str = "standard"
):
    """Trigger video analysis pipeline"""

    video = await get_video(video_id)

    if level == "quick":
        # Quick preview
        tasks = [
            analyze_scenes(video),
            extract_keyframes(video)
        ]

    elif level == "standard":
        # Standard analysis
        tasks = [
            analyze_scenes(video),
            extract_keyframes(video),
            transcribe_audio(video),
            detect_importance(video),
            detect_characters(video)
        ]

    elif level == "deep":
        # Deep analysis
        tasks = [
            analyze_scenes(video),
            extract_keyframes(video),
            transcribe_audio(video),
            detect_importance(video),
            detect_characters(video),
            generate_summary(video),
            identify_themes(video),
            map_character_relationships(video)
        ]

    # Run tasks in background
    task_id = await run_async_tasks(tasks)

    return {
        "task_id": task_id,
        "estimated_time": estimate_analysis_time(level, video.duration)
    }
```

---

## 🎨 Complete Upload Flow Diagram

```
User Opens App
     │
     ├─→ Has No Videos?
     │   └─→ Show Upload Zone
     │       ├─→ Drag & Drop
     │       ├─→ Choose File
     │       ├─→ Import from URL
     │       └─→ Cloud Storage
     │
     ├─→ Has Videos?
     │   └─→ Show Video Library
     │       ├─→ [+ Upload New]
     │       └─→ Select Existing Video
     │
     ▼
File Selected
     │
     ├─→ Validate
     │   ├─→ Format OK?
     │   ├─→ Size OK?
     │   └─→ Already exists?
     │
     ▼
Initialize Upload
     │
     ├─→ Create session
     ├─→ Calculate chunks
     └─→ Show progress UI
     │
     ▼
Upload Chunks
     │
     ├─→ Upload chunk 1/20 ✓
     ├─→ Upload chunk 2/20 ✓
     ├─→ Upload chunk 3/20 🔄
     │   ├─→ User can pause
     │   ├─→ User can resume
     │   └─→ User can cancel
     │
     ▼
Upload Complete
     │
     ├─→ Merge chunks
     ├─→ Verify integrity
     └─→ Create video record
     │
     ▼
Choose Analysis Level
     │
     ├─→ Quick (1-2 min)
     ├─→ Standard (5-10 min)
     ├─→ Deep (15-30 min)
     └─→ Skip for now
     │
     ▼
Run Analysis
     │
     ├─→ Scene detection ✓
     ├─→ Keyframe extraction ✓
     ├─→ Transcription 🔄
     ├─→ Importance analysis ⏳
     └─→ AI summary ⏳
     │
     ▼
Analysis Complete
     │
     └─→ Open Video in Player
         ├─→ Timeline ready
         ├─→ Scenes detected
         └─→ Ready for annotation
```

---

## ✅ Summary

### Upload Methods:
1. **📤 Local File Upload** - Drag & drop or file picker
2. **🌐 URL Import** - Download from URL
3. **☁️ Cloud Storage** - Google Drive, Dropbox, OneDrive, S3

### Features:
- ✅ Chunked upload for large files
- ✅ Pause/resume capability
- ✅ Real-time progress tracking
- ✅ File validation & deduplication
- ✅ Automatic analysis trigger
- ✅ Video library management
- ✅ Analysis level selection

### User Experience:
- Simple drag & drop interface
- Clear progress indicators
- Estimated time remaining
- Background processing
- Automatic thumbnail generation
- Quick access to uploaded videos

**Ready to implement!** 🚀
