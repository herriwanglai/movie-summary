# METEORA LX - Agents Implementation Plan

## Overview
This document outlines the multi-agent development strategy with specialized agents, each with documentation sub-agents for faster reference and best practices.

---

## Agent Architecture Pattern

Each agent follows this structure:

```
MAIN AGENT
├── Skills.md (task definition & responsibilities)
├── Documentation Sub-Agent (learns & references docs)
└── Implementation Tasks
```

**Benefits:**
- Main agent focuses on implementation
- Doc sub-agent provides instant best practices reference
- Faster development with accurate documentation
- Consistent code quality

---

## Development Phases

### **PHASE 1: Frontend Foundation** ✅
**Status:** COMPLETE
**Duration:** Setup complete
**Deliverables:**
- ✅ React + TypeScript + Vite initialized
- ✅ Tailwind CSS v4 with dark theme
- ✅ shadcn/ui dependencies installed
- ✅ Path aliases configured
- ✅ Basic app structure with METEORA LX branding

---

### **PHASE 2: Parallel Agent Development (MVP)**
**Goal:** Get video upload working end-to-end
**Strategy:** 3 parallel agents with documentation sub-agents

---

## 🤖 Agent 1: Frontend Components & UI

### **Agent Skills** (`agents/agent-1-frontend/SKILLS.md`)

**Primary Responsibility:**
Build core React components and UI features for METEORA LX

**Tech Stack:**
- React 19 + TypeScript
- shadcn/ui components
- Tailwind CSS v4 (dark mode)
- Zustand (state management)
- React Router (navigation)

**Key Tasks:**
1. Install and configure shadcn/ui components
2. Create video upload UI with progress tracking
3. Build basic video player component
4. Implement file drag-and-drop interface
5. Create loading states and error boundaries
6. Set up Zustand stores for state management
7. Build responsive layouts

**Documentation Sub-Agent Tasks:**
- Learn React 19 best practices and hooks
- Study shadcn/ui component patterns
- Research Tailwind CSS v4 @theme syntax
- Find best practices for TypeScript with React
- Learn Zustand state management patterns
- Study accessibility guidelines for video players

**Success Criteria:**
- Upload UI accepts video files with drag-and-drop
- Progress bar shows upload status
- Video player can play uploaded videos
- Components follow shadcn/ui patterns
- Dark theme renders correctly across all components
- TypeScript has no errors

**Estimated Implementation:**
- shadcn/ui setup: 30 min
- Upload UI: 1-2 hours
- Video player integration: 2-3 hours
- State management setup: 1 hour
- Testing & refinement: 1 hour

---

## 🤖 Agent 2: Backend API & Upload System

### **Agent Skills** (`agents/agent-2-backend/SKILLS.md`)

**Primary Responsibility:**
Build FastAPI backend with chunked video upload system

**Tech Stack:**
- FastAPI (Python 3.11+)
- SQLAlchemy (ORM)
- Alembic (migrations)
- PostgreSQL or SQLite
- Pydantic (validation)
- python-multipart (file uploads)

**Key Tasks:**
1. Set up FastAPI project structure
2. Create database models (Video, Scene, Screenshot, Clip, Annotation)
3. Implement chunked upload endpoints
   - POST /api/upload/init
   - POST /api/upload/chunk
   - POST /api/upload/complete
4. File validation and storage
5. Upload session management
6. CORS configuration for frontend
7. Health check and status endpoints
8. API documentation (auto-generated)

**Documentation Sub-Agent Tasks:**
- Learn FastAPI best practices and project structure
- Study chunked file upload patterns
- Research SQLAlchemy relationship patterns
- Learn Pydantic validation best practices
- Study async/await patterns in FastAPI
- Find optimal file storage strategies

**Success Criteria:**
- Backend API starts without errors
- Upload endpoints accept chunked files
- Files reassemble correctly after upload
- Database stores video metadata
- API docs accessible at /docs
- CORS allows frontend origin
- Upload progress tracking works

**Estimated Implementation:**
- FastAPI setup: 1 hour
- Database models: 1-2 hours
- Chunked upload system: 3-4 hours
- File validation: 1 hour
- Testing endpoints: 1 hour

---

## 🤖 Agent 3: Video Processing Pipeline

### **Agent Skills** (`agents/agent-3-video-processing/SKILLS.md`)

**Primary Responsibility:**
Complete video processing pipeline for scene detection and keyframe extraction

**Tech Stack:**
- FFmpeg (video manipulation)
- OpenCV (frame extraction)
- PySceneDetect (scene detection)
- NumPy (numerical operations)
- Pillow (image processing)

**Key Tasks:**
1. Complete `video_processor/extractor.py`
   - Extract frames at specified intervals
   - Generate thumbnails
2. Complete `video_processor/scene_detector.py`
   - Detect scene transitions
   - Identify scene boundaries
3. Complete `video_processor/keyframe_selector.py`
   - Select representative keyframes per scene
4. Complete `video_processor/importance_detector.py`
   - Calculate visual intensity
   - Calculate audio intensity
   - Analyze dialogue density
5. Integrate with backend upload workflow
6. Add processing status updates

**Documentation Sub-Agent Tasks:**
- Learn FFmpeg command-line usage and Python bindings
- Study PySceneDetect API and scene detection algorithms
- Research keyframe extraction strategies
- Learn OpenCV frame manipulation techniques
- Study video metadata extraction
- Find performance optimization techniques

**Success Criteria:**
- Can extract frames from uploaded videos
- Scene detection identifies transitions accurately
- Keyframes are selected intelligently
- Importance scores calculated for scenes
- Processing completes in reasonable time
- Status updates sent to frontend

**Estimated Implementation:**
- Frame extraction: 1-2 hours
- Scene detection integration: 2 hours
- Keyframe selection: 1-2 hours
- Importance detector: 2-3 hours
- Integration with upload: 1 hour
- Performance optimization: 1 hour

---

## 🔄 Agent Coordination & Workflow

### **Parallel Execution Flow:**

```
START
  │
  ├─► AGENT 1: Frontend Components
  │   ├─► Doc Sub-Agent: Learn React 19 + shadcn/ui
  │   └─► Build upload UI + video player
  │
  ├─► AGENT 2: Backend API
  │   ├─► Doc Sub-Agent: Learn FastAPI + SQLAlchemy
  │   └─► Build upload endpoints + database
  │
  └─► AGENT 3: Video Processing
      ├─► Doc Sub-Agent: Learn FFmpeg + PySceneDetect
      └─► Complete video processing pipeline
      │
      ▼
INTEGRATION POINT
  │
  └─► Test end-to-end video upload flow
      ├─► Frontend sends video chunks
      ├─► Backend receives and stores
      ├─► Processing extracts frames/scenes
      └─► Frontend displays results
      │
      ▼
MVP COMPLETE: Video Upload Working
```

---

## 📋 Implementation Checklist

### **Pre-Execution Setup**
- [ ] Create agent skills.md files in `/agents/` directory
- [ ] Set up branch strategy (one branch per agent or shared branch?)
- [ ] Define integration points and handoff criteria
- [ ] Prepare test video files for validation

### **Agent 1 Deliverables**
- [ ] shadcn/ui Button, Card, Progress, Dialog components installed
- [ ] Upload UI with drag-and-drop
- [ ] Progress bar component
- [ ] Video player component (Plyr or video.js)
- [ ] Zustand store for upload state
- [ ] Error handling UI

### **Agent 2 Deliverables**
- [ ] FastAPI app with project structure
- [ ] SQLAlchemy models (Video, metadata)
- [ ] Database migrations (Alembic)
- [ ] POST /api/upload/init endpoint
- [ ] POST /api/upload/chunk endpoint
- [ ] POST /api/upload/complete endpoint
- [ ] GET /api/videos endpoint
- [ ] GET /api/health endpoint

### **Agent 3 Deliverables**
- [ ] Completed VideoFrameExtractor class
- [ ] Completed SceneDetector class
- [ ] Completed KeyframeSelector class
- [ ] Completed ImportanceDetector class
- [ ] Integration with upload complete event
- [ ] Processing status updates

### **Integration Testing**
- [ ] Frontend can upload 100MB+ video
- [ ] Backend receives all chunks correctly
- [ ] File reassembles without corruption
- [ ] Processing pipeline triggers automatically
- [ ] Scenes and keyframes extracted
- [ ] Results displayed in frontend

---

## 📊 Estimated Timeline

### **Parallel Phase (All agents working simultaneously)**

| Agent | Focus Area | Estimated Time |
|-------|-----------|----------------|
| Agent 1 | Frontend UI | 5-7 hours |
| Agent 2 | Backend API | 7-9 hours |
| Agent 3 | Video Processing | 8-10 hours |

**Effective Time with Parallelization:** 8-10 hours (instead of 20-26 sequential)

### **Integration Phase (Sequential)**

| Task | Estimated Time |
|------|----------------|
| Connect frontend to backend | 1 hour |
| Test upload flow | 1 hour |
| Debug integration issues | 1-2 hours |
| Verify processing pipeline | 1 hour |

**Integration Time:** 4-5 hours

### **Total MVP Time:** 12-15 hours of work

With 3 agents in parallel, this could complete in a single development session or 1-2 days depending on testing thoroughness.

---

## 🎯 MVP Success Definition

The MVP is complete when:

1. **User can upload a video file**
   - Drag-and-drop or file picker
   - Progress bar shows upload status
   - Large files (1GB+) upload successfully

2. **Backend processes the video**
   - File stored safely
   - Metadata extracted
   - Database record created

3. **Video processing extracts data**
   - Scenes detected
   - Keyframes extracted
   - Importance scores calculated

4. **Results visible in UI**
   - Video playable in browser
   - Scenes listed with timestamps
   - Keyframes displayed as thumbnails

---

## 🚀 Next Phases (After MVP)

Once video upload MVP is working, proceed with:

### **Phase 3: Timeline & Navigation (2-3 agents)**
- Agent 4: Magnetic Timeline component
- Agent 5: Global navigation system
- Agent 6: Keyboard shortcuts

### **Phase 4: AI Features (3 agents)**
- Agent 7: Subtitle detection & transcription
- Agent 8: AI caption generator (Ollama + LLaVA)
- Agent 9: Character pose/expression detection

### **Phase 5: Export & Polish (2 agents)**
- Agent 10: Ink script generator
- Agent 11: Export system (PDF, images, clips)

---

## 📝 Agent Communication Protocol

### **Handoff Points:**
1. **Agent 2 → Agent 1:** API endpoint contracts defined (OpenAPI spec)
2. **Agent 2 → Agent 3:** Upload complete event trigger
3. **Agent 3 → Agent 2:** Processing results storage format

### **Shared Resources:**
- Database schema (Agent 2 defines, Agent 3 uses)
- API contracts (Agent 2 defines, Agent 1 consumes)
- File storage structure (Agent 2 creates, Agent 3 reads)

### **Integration Points:**
- Frontend API client (Agent 1 implements against Agent 2's spec)
- Processing trigger (Agent 2 calls Agent 3's functions)
- Results display (Agent 1 displays Agent 3's output)

---

## ✅ Agent Task Completion Criteria

Each agent must:
1. Complete all deliverables in their skills.md
2. Pass unit tests (where applicable)
3. Commit code with clear messages
4. Document any API changes
5. Provide integration notes for other agents
6. Update system status in App.tsx

**Ready to launch agents?**

### Recommended Execution Command:
```
Launch 3 agents in parallel:
- Agent 1: Frontend Components
- Agent 2: Backend API
- Agent 3: Video Processing

Each with their documentation sub-agent for best practices reference.
```
