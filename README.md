# METEORA LX

**AI-Powered Movie Analysis Platform**

A comprehensive video analysis tool that combines scene detection, keyframe extraction, and AI-powered insights for filmmakers, editors, and content creators.

---

## 🎬 Features

### MVP (Phase 1) - ✅ Complete
- ✅ **Video Upload** - Drag-and-drop interface with TUS resumable uploads
- ✅ **Video Player** - Full-featured player with screenshot capture
- ✅ **Scene Detection** - Automatic scene boundary detection
- ✅ **Keyframe Extraction** - Intelligent frame selection
- ✅ **Dark Mode UI** - Cinematic dark theme throughout

### Coming Soon
- 🔄 **Magnetic Timeline** - Final Cut Pro-style timeline navigation
- 🔄 **AI Captions** - Generate captions, dialog, quotes with Ollama
- 🔄 **Character Analysis** - Pose and expression detection
- 🔄 **Ink Export** - Export to Ink visual novel format
- 🔄 **Collection Manager** - Organize screenshots and clips

---

## 🚀 Quick Start (macOS)

### Prerequisites
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required tools
brew install python@3.11 node ffmpeg git
```

### Setup

```bash
# 1. Clone the repository
git clone <your-repo-url> movie-summary
cd movie-summary

# 2. Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdir -p videos

# 3. Frontend setup
cd ../frontend
npm install

# 4. Start both servers (from project root)
cd ..
./start.sh
```

**Or start manually:**

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Access the Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 📚 Documentation

- **[Local Setup Guide (macOS)](LOCAL_SETUP_MACOS.md)** - Detailed setup instructions
- **[MVP Completion Summary](MVP_COMPLETION_SUMMARY.md)** - Technical details and achievements
- **[Project Timeline](PROJECT_TIMELINE_SUMMARY.md)** - Development phases and estimates
- **[Testing Strategy](TESTING_STRATEGY_PLAYWRIGHT.md)** - Playwright testing approach
- **[Agents Implementation](AGENTS_IMPLEMENTATION.md)** - Multi-agent development plan

---

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- React 19 + TypeScript
- Vite (build tool)
- Tailwind CSS v4 (dark mode)
- shadcn/ui components
- Zustand (state management)

**Backend:**
- FastAPI (Python 3.11+)
- tuspyserver (TUS resumable uploads)
- SQLAlchemy 2.0 (ORM)
- SQLite (dev) / PostgreSQL (prod)

**Video Processing:**
- FFmpeg (video manipulation)
- OpenCV (frame extraction)
- PySceneDetect (scene detection)
- NumPy + Pillow (image processing)

### Project Structure

```
movie-summary/
├── frontend/           # React frontend
│   ├── src/
│   │   ├── components/ # UI components
│   │   ├── stores/     # Zustand stores
│   │   └── App.tsx     # Main app
│   └── package.json
│
├── backend/            # FastAPI backend
│   ├── app/
│   │   ├── main.py     # FastAPI app
│   │   ├── models/     # Database models
│   │   ├── routers/    # API endpoints
│   │   └── services/   # Business logic
│   └── requirements.txt
│
├── src/                # Video processing
│   └── video_processor/
│       ├── pipeline.py         # Main pipeline
│       ├── scene_detector.py   # Scene detection
│       └── keyframe_selector.py
│
└── agents/             # Agent implementation docs
```

---

## 🧪 Testing

### Manual Testing

**Test Video Player:**
1. Open http://localhost:5173
2. Click "Show Player Demo"
3. Demo video should play

**Test Video Upload:**
1. Click "Show Uploader"
2. Drag and drop a video file
3. Click "Upload Video"

**Test Backend API:**
```bash
# Health check
curl http://localhost:8000/api/health

# List videos
curl http://localhost:8000/api/videos/

# View API docs
open http://localhost:8000/docs
```

---

## 📊 Development Status

**Phase 1: MVP** ✅ Complete (10-12 hours)

**Phase 2: Timeline & Navigation** (6-8 hours)

**Phase 3: Collection & Node Editor** (5-6 hours)

**Phase 4: AI Features** (6-8 hours)

**Phase 5: Ink Export** (5-6 hours)

See [PROJECT_TIMELINE_SUMMARY.md](PROJECT_TIMELINE_SUMMARY.md) for details.

---

## 🐛 Troubleshooting

See [LOCAL_SETUP_MACOS.md](LOCAL_SETUP_MACOS.md) for detailed troubleshooting.

**Quick fixes:**
```bash
# Kill processes on ports
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:5173 | xargs kill -9  # Frontend

# Reset database
cd backend && rm meteora_lx.db

# Reinstall dependencies
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

---

**Last Updated:** January 6, 2026  
**Version:** 0.1.0 (MVP)  
**Status:** ✅ Ready for local development
