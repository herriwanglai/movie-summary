# METEORA LX - Video Upload & Playback Testing Guide

## Quick Start

### 1. Start the Application

```bash
# Make sure Docker is running
docker compose up -d

# Check that all services are running
docker compose ps

# Should show:
# - frontend (port 3000)
# - backend (port 8000)
# - postgres (port 5432)
```

### 2. Access the Frontend

Open your browser and go to:
```
http://localhost:3000
```

You should see the METEORA LX welcome screen with three buttons:
- **Show Uploader** - Test video upload functionality
- **Show Player Demo** - Test video player with a demo video
- **Phase 2: Timeline Demo** - Test full timeline workspace

---

## Testing Video Upload

### Step-by-Step Instructions

1. **Click "Show Uploader" button**
   - The video uploader interface will appear below

2. **Select a Video File** (two methods):

   **Method A: Drag & Drop**
   - Drag a video file from your file explorer
   - Drop it into the dashed border area

   **Method B: Browse Files**
   - Click the "Browse Files" button
   - Select a video file from your computer

3. **File Validation**
   - Supported formats: MP4, MOV, AVI, MKV
   - Maximum size: 10GB
   - File type must be `video/*`

4. **Upload the Video**
   - After selecting a file, you'll see:
     - File name
     - File size
     - "Upload Video" button
   - Click "Upload Video" to start

5. **Monitor Upload Progress**
   - Progress bar shows upload percentage
   - Upload uses TUS protocol (resumable uploads)
   - 5MB chunks for reliable transfer

### What Happens During Upload

```
Frontend (VideoUploader.tsx)
  ↓ [TUS protocol - resumable upload]
  ↓ [Sends to: http://localhost:8000/api/upload/files/]
Backend (FastAPI + TUS)
  ↓ [Saves to: ./videos/ directory]
  ↓ [Creates database record]
Database (PostgreSQL)
  ↓ [Stores video metadata]
  ✅ Upload Complete
```

### Upload Component Details

**Location**: `frontend/src/components/upload/VideoUploader.tsx`

**Key Features**:
- TUS resumable upload protocol
- Drag & drop support
- File validation (type, size)
- Progress tracking
- Automatic retry on failure (3s, 5s, 10s, 20s delays)
- Resume interrupted uploads

**Backend Endpoint**: `POST http://localhost:8000/api/upload/files/`

**Request Metadata**:
```json
{
  "filename": "my-video.mp4",
  "filetype": "video/mp4",
  "filesize": "104857600"
}
```

---

## Testing Video Playback

### Step-by-Step Instructions

1. **Click "Show Player Demo" button**
   - The video player will appear with a demo video
   - Demo video: Big Buck Bunny (from Google CDN)

2. **Player Controls**
   - Play/Pause button
   - Volume control
   - Seek bar (scrub timeline)
   - Fullscreen toggle
   - Speed controls (0.5x, 1x, 1.5x, 2x)

3. **Test Features**:
   - **Playback**: Click play and watch video
   - **Seeking**: Click anywhere on the timeline
   - **Volume**: Adjust volume slider
   - **Screenshot**: Press 'S' key or use screenshot button

### Player Component Details

**Location**: `frontend/src/components/player/VideoPlayer.tsx`

**Technology**: Vidstack Player (modern video player)

**Key Features**:
- HLS & DASH support
- Keyboard shortcuts
- Screenshot capture
- Time tracking callbacks
- Responsive design

**Props**:
```typescript
<VideoPlayer
  src="https://example.com/video.mp4"  // Video URL
  title="My Video"                       // Display title
  onScreenshot={(dataUrl, timestamp) => {}} // Screenshot callback
  onTimeUpdate={(time) => {}}           // Playback time callback
/>
```

---

## Testing Full Timeline Workspace (Phase 2)

### Step-by-Step Instructions

1. **Click "Phase 2: Timeline Demo" button**
   - Full-screen workspace will open
   - Shows integrated timeline + player

2. **Timeline Features**:
   - **Magnetic Timeline**: Scene markers that snap to playhead
   - **Scene Navigator**: Visual scene thumbnails
   - **Playback Controls**: Enhanced controls with frame stepping

3. **Keyboard Shortcuts**:
   - `Space` - Play/Pause
   - `←/→` - Seek backward/forward 5 seconds
   - `↑/↓` - Increase/decrease volume
   - `F` - Toggle fullscreen
   - `S` - Take screenshot
   - `M` - Mute/unmute

### Workspace Component Details

**Location**: `frontend/src/components/workspace/VideoWorkspace.tsx`

**Components Used**:
- `VideoPlayer` - Main video playback
- `MagneticTimeline` - Interactive timeline with scene markers
- `SceneNavigator` - Scene thumbnail grid
- `PlaybackControls` - Enhanced playback controls

**State Management**:
- `playerStore` - Video playback state
- `timelineStore` - Timeline & scene data
- `videoStore` - Video metadata

---

## Backend API Testing

### Check Backend Status

```bash
# Test backend health
curl http://localhost:8000/api/health

# Expected response:
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### Upload API Endpoint

```bash
# TUS upload endpoint (handled by tuspyserver)
# Endpoint: http://localhost:8000/api/upload/files/

# The frontend handles TUS protocol automatically
# You can test with curl if needed (see TUS documentation)
```

### Videos API Endpoints

```bash
# List all videos
curl http://localhost:8000/api/videos

# Get specific video
curl http://localhost:8000/api/videos/{video_id}

# Get video stream
curl http://localhost:8000/api/videos/{video_id}/stream
```

---

## Troubleshooting

### Frontend Not Loading

**Issue**: `http://localhost:3000` not accessible

**Solution**:
```bash
# Check if frontend container is running
docker compose ps frontend

# Check frontend logs
docker compose logs frontend

# If you see "@/lib/utils" import errors, run:
./COMPLETE_FIX.sh
```

### Upload Fails

**Issue**: Upload shows error message

**Possible Causes**:
1. Backend not running → Check `docker compose ps backend`
2. CORS error → Check backend logs
3. File too large → Max 10GB
4. Wrong file type → Must be `video/*`

**Debug**:
```bash
# Check backend logs
docker compose logs backend

# Check upload directory
ls -la videos/

# Test backend directly
curl http://localhost:8000/api/health
```

### Video Won't Play

**Issue**: Player shows but video doesn't load

**Possible Causes**:
1. Invalid video URL
2. CORS issue with external video
3. Video format not supported

**Debug**:
- Open browser DevTools (F12)
- Check Console for errors
- Check Network tab for failed requests

---

## File Structure Reference

```
frontend/
├── src/
│   ├── components/
│   │   ├── upload/
│   │   │   └── VideoUploader.tsx    # Video upload UI
│   │   ├── player/
│   │   │   └── VideoPlayer.tsx      # Video player
│   │   ├── timeline/
│   │   │   ├── MagneticTimeline.tsx # Timeline with markers
│   │   │   ├── SceneNavigator.tsx   # Scene thumbnails
│   │   │   └── PlaybackControls.tsx # Enhanced controls
│   │   └── workspace/
│   │       └── VideoWorkspace.tsx   # Full timeline workspace
│   ├── stores/
│   │   ├── playerStore.ts           # Player state
│   │   ├── timelineStore.ts         # Timeline state
│   │   └── videoStore.ts            # Video metadata
│   └── App.tsx                       # Main app with demos

backend/
├── app/
│   ├── main.py                       # FastAPI app
│   ├── routers/
│   │   ├── videos.py                 # Video API endpoints
│   │   └── health.py                 # Health check
│   └── services/
│       └── upload_handler.py         # Upload processing
└── videos/                            # Upload directory
```

---

## Expected Behavior Summary

### ✅ Working Features

1. **Video Upload**
   - Select file via drag-drop or browse
   - Upload progress tracking
   - TUS resumable uploads
   - File validation

2. **Video Player**
   - Play/pause demo video
   - Seek timeline
   - Volume control
   - Screenshot capture
   - Keyboard shortcuts

3. **Timeline Workspace**
   - Full-screen video player
   - Magnetic timeline with markers
   - Scene navigation
   - Enhanced playback controls

### 🔄 In Progress Features

- Backend video processing
- Scene detection AI
- Video transcription
- Analysis results display

---

## Next Steps

1. **Test Upload Flow**:
   ```bash
   # Start services
   docker compose up -d

   # Access frontend
   open http://localhost:3000

   # Click "Show Uploader"
   # Upload a test video
   ```

2. **Test Playback**:
   ```bash
   # Click "Show Player Demo"
   # Verify demo video plays
   ```

3. **Test Timeline**:
   ```bash
   # Click "Phase 2: Timeline Demo"
   # Test keyboard shortcuts
   # Navigate scenes
   ```

---

## Support

If you encounter issues:

1. **Check Docker logs**: `docker compose logs`
2. **Run fix script**: `./COMPLETE_FIX.sh`
3. **Verify services**: `docker compose ps`
4. **Check browser console**: Open DevTools (F12)

For import errors specifically, see `REACT_UI_STRUCTURE.md` for component documentation.
