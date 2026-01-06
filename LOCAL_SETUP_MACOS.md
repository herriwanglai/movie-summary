# METEORA LX - Local Setup Guide (macOS)

## 🍎 Running METEORA LX on Your Mac

Complete guide to set up and run the METEORA LX MVP on macOS.

---

## 📋 Prerequisites

### 1. Install Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Required Software

**Python 3.11+:**
```bash
brew install python@3.11
# Verify installation
python3 --version  # Should be 3.11 or higher
```

**Node.js 18+:**
```bash
brew install node
# Verify installation
node --version  # Should be 18 or higher
npm --version
```

**FFmpeg (for video processing):**
```bash
brew install ffmpeg
# Verify installation
ffmpeg -version
```

**Git (if not installed):**
```bash
brew install git
```

---

## 🚀 Setup Instructions

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <your-repo-url> movie-summary
cd movie-summary

# Checkout the MVP branch
git checkout claude/movie-analysis-ollama-tools-SayCP
```

---

### Step 2: Backend Setup (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create videos directory for uploads
mkdir -p videos

# Initialize database
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"

# Run database migrations (if needed)
# alembic upgrade head
```

**Start the backend server:**
```bash
# Make sure you're in the backend directory with venv activated
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Test the backend:**
Open a new terminal tab and run:
```bash
curl http://localhost:8000/api/health
# Should return: {"status":"healthy","service":"METEORA LX API"}
```

**View API documentation:**
Open in browser: http://localhost:8000/docs

---

### Step 3: Frontend Setup (React + Vite)

Open a **new terminal tab/window** (keep backend running):

```bash
# Navigate to frontend directory
cd movie-summary/frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

You should see:
```
VITE v7.2.4  ready in XXX ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

**Open the application:**
Open your browser to: http://localhost:5173

---

## 🎬 Using the Application

### 1. Test Video Player Demo
1. Click "Show Player Demo" button
2. Demo video should load and play (Big Buck Bunny)
3. Test controls: play, pause, volume, fullscreen

### 2. Test Video Upload
1. Click "Show Uploader" button
2. Drag and drop a video file OR click "Browse Files"
3. Click "Upload Video"
4. Watch progress bar (currently simulated)

---

## 🔧 Common Issues & Solutions

### Issue: Port Already in Use

**Backend (port 8000):**
```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --reload --port 8001
```

**Frontend (port 5173):**
```bash
# Find process using port 5173
lsof -ti:5173 | xargs kill -9

# Or use different port
npm run dev -- --port 3000
```

### Issue: Python Module Not Found

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Node Modules Missing

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue: Database Errors

```bash
# Delete and recreate database
cd backend
rm meteora_lx.db
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### Issue: FFmpeg Not Found

```bash
# Install FFmpeg
brew install ffmpeg

# Verify installation
which ffmpeg
ffmpeg -version
```

---

## 📂 Project Structure

```
movie-summary/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Main FastAPI app
│   │   ├── models/         # Database models
│   │   ├── routers/        # API endpoints
│   │   └── services/       # Business logic
│   ├── requirements.txt    # Python dependencies
│   └── videos/             # Upload directory
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── stores/         # Zustand stores
│   │   └── App.tsx         # Main app component
│   ├── package.json        # Node dependencies
│   └── vite.config.ts      # Vite configuration
│
└── src/                    # Video processing pipeline
    └── video_processor/
```

---

## 🧪 Testing the MVP

### Test Backend API

```bash
# Health check
curl http://localhost:8000/api/health

# List videos (should be empty initially)
curl http://localhost:8000/api/videos/

# View API docs
open http://localhost:8000/docs
```

### Test Frontend

1. **Open browser:** http://localhost:5173
2. **Verify components:**
   - ✅ METEORA LX title displays
   - ✅ System Status shows "ready" for frontend
   - ✅ Both buttons (Uploader/Player) work
3. **Test player:**
   - Click "Show Player Demo"
   - Video should load and play
4. **Test uploader:**
   - Click "Show Uploader"
   - UI should show drag-drop zone

---

## 🔄 Next Steps: Integration

Currently, the frontend upload is **simulated**. To connect it to the real backend:

### Option 1: Install TUS Client (Recommended)

```bash
cd frontend
npm install tus-js-client
```

Then update `frontend/src/components/upload/VideoUploader.tsx` to use real TUS upload (see integration notes in MVP_COMPLETION_SUMMARY.md).

### Option 2: Test with curl

```bash
# Create a small test video
# Then upload via TUS protocol (requires tus-js-client or similar)
```

---

## 🛑 Stopping the Servers

### Stop Backend:
In the backend terminal, press `Ctrl+C`

### Stop Frontend:
In the frontend terminal, press `Ctrl+C`

### Deactivate Python Virtual Environment:
```bash
deactivate
```

---

## 🚀 Quick Start Script

Create a file `start.sh` in the project root:

```bash
#!/bin/bash

# Start backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "🎬 METEORA LX is starting..."
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
```

Make it executable and run:
```bash
chmod +x start.sh
./start.sh
```

---

## 📊 System Requirements

**Minimum:**
- macOS 10.15+ (Catalina or later)
- 8GB RAM
- 5GB free disk space

**Recommended:**
- macOS 12+ (Monterey or later)
- 16GB RAM
- 20GB free disk space (for video processing)

---

## 🆘 Getting Help

### Check Logs

**Backend logs:**
```bash
# Terminal will show logs directly
# Or check uvicorn output
```

**Frontend logs:**
```bash
# Check browser console (F12 > Console tab)
# Or check terminal for build errors
```

### Verify Services

```bash
# Check if backend is running
curl http://localhost:8000/api/health

# Check if frontend is running
curl http://localhost:5173
```

### Common Commands

```bash
# Backend: Restart server
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Frontend: Rebuild
cd frontend
rm -rf node_modules
npm install
npm run dev

# Database: Reset
cd backend
rm meteora_lx.db
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

---

## 🎯 Current MVP Status

**✅ Working:**
- Backend API with health check
- Frontend UI with dark theme
- Video player with demo video
- Upload UI (simulated progress)

**⚠️ Pending Integration:**
- Real TUS upload connection
- Video processing trigger
- Database storage of results

**Next Phase:**
- Connect frontend to backend TUS endpoint
- Trigger video processing on upload
- Display processed results in UI

---

## 📝 Environment Variables (Optional)

Create `backend/.env` for custom configuration:

```bash
# Database
DATABASE_URL=sqlite:///./meteora_lx.db

# Upload settings
VIDEO_DIR=videos
MAX_UPLOAD_SIZE=10737418240  # 10GB in bytes

# CORS
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Server
HOST=0.0.0.0
PORT=8000
```

---

## 🔐 Security Notes

For development only:
- Backend runs on `localhost:8000`
- Frontend runs on `localhost:5173`
- No authentication required
- SQLite database (not for production)

For production deployment, you'll need:
- PostgreSQL database
- Environment variables for secrets
- HTTPS/SSL certificates
- Authentication/authorization
- CORS restrictions

---

**Last Updated:** January 6, 2026
**Project:** METEORA LX MVP
**Status:** Ready for local development

For issues or questions, check `MVP_COMPLETION_SUMMARY.md` for technical details.
