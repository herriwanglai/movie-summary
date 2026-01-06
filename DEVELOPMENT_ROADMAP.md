# METEORA LX - Development Roadmap & Milestones

## Project Overview
**METEORA LX** - AI-Powered Movie Analysis Platform with Ollama deepseek-r1:8b

---

## Development Phases & Milestones

### 🏗️ **PHASE 1: FOUNDATION**
**Goal:** Establish core infrastructure for both frontend and backend

#### Milestone 1.1: Frontend Foundation ✅ (IN PROGRESS)
**Status:** Setup initiated
**Deliverables:**
- [x] React 19 + TypeScript + Vite project initialized
- [x] Tailwind CSS v4 with cinematic dark theme configured
- [x] shadcn/ui dependencies installed
- [ ] Path aliases configured in Vite
- [ ] Component library structure created (`components/ui/`)
- [ ] Utility functions setup (`lib/utils.ts`)
- [ ] Basic routing structure (React Router)
- [ ] State management setup (Zustand stores)

**Review Checkpoint:**
- Verify dark theme renders correctly
- Test component imports with @ alias
- Confirm hot module replacement works
- Check build process completes without errors

---

#### Milestone 1.2: Backend Foundation
**Status:** Pending
**Deliverables:**
- [ ] FastAPI project structure created
- [ ] Database models defined (SQLAlchemy)
  - Video metadata model
  - Scene model
  - Screenshot/Clip models
  - Annotation model
  - Subtitle model
- [ ] Database migrations setup (Alembic)
- [ ] CORS middleware configured
- [ ] Environment configuration (.env)
- [ ] Health check endpoint (`/api/health`)
- [ ] API documentation (auto-generated with FastAPI)

**Review Checkpoint:**
- API responds to health check
- Database connection successful
- OpenAPI docs accessible at `/docs`
- CORS allows frontend origin

---

#### Milestone 1.3: Video Processing Pipeline
**Status:** Partially complete (design done)
**Deliverables:**
- [ ] Complete `video_processor/extractor.py` implementation
- [ ] Complete `video_processor/scene_detector.py` implementation
- [ ] Complete `video_processor/keyframe_selector.py` implementation
- [ ] Complete `video_processor/importance_detector.py` implementation
- [ ] FFmpeg integration for frame extraction
- [ ] PySceneDetect integration for scene detection
- [ ] Visual/audio intensity calculation
- [ ] Unit tests for video processing modules

**Review Checkpoint:**
- Successfully extract frames from test video
- Scene detection identifies transitions correctly
- Importance scores calculated for test scenes
- Processing speed is acceptable (benchmark)

---

### 🎬 **PHASE 2: VIDEO PLAYER & TIMELINE**
**Goal:** Build core video playback and navigation features

#### Milestone 2.1: Video Upload System
**Status:** Design complete
**Deliverables:**
- [ ] Chunked upload API endpoint (`/api/upload/chunk`)
- [ ] Upload session management
- [ ] File validation (format, size)
- [ ] Progress tracking (WebSocket/Server-Sent Events)
- [ ] Video file storage organization
- [ ] Upload UI component with progress bar
- [ ] Pause/resume upload functionality
- [ ] Deduplication check (hash-based)

**Review Checkpoint:**
- Upload 1GB+ video successfully
- Pause and resume works correctly
- Progress updates in real-time
- Duplicate detection prevents re-upload

---

#### Milestone 2.2: Magnetic Timeline Component
**Status:** Design complete
**Deliverables:**
- [ ] Timeline core component (`MagneticTimeline.tsx`)
- [ ] Multi-track system (scenes, screenshots, clips, annotations)
- [ ] Horizontal scroll with smooth performance
- [ ] Snap-to-keyframe algorithm
- [ ] Timeline markers for different content types
- [ ] Zoom in/out functionality
- [ ] Playhead synchronization with video
- [ ] Waveform visualization (optional enhancement)

**Review Checkpoint:**
- Timeline renders 100+ markers smoothly
- Snap behavior works like Final Cut Pro
- Clicking timeline seeks video correctly
- Multi-track layout is visually clear

---

#### Milestone 2.3: Video Player Integration
**Status:** Design complete
**Deliverables:**
- [ ] Video player component (Plyr or video.js)
- [ ] Custom control overlays
- [ ] Screenshot capture functionality
  - Single frame capture
  - Save as PNG with timestamp
  - Add to collection automatically
- [ ] Clip selection mode
  - Mark in/out points
  - Trim preview
  - Save clip metadata (no re-encoding yet)
- [ ] Playback controls (play, pause, seek, speed)
- [ ] Volume and fullscreen controls

**Review Checkpoint:**
- Video plays smoothly without stuttering
- Screenshots capture at exact frame
- Clip in/out marking is intuitive
- Player controls are responsive

---

### 📸 **PHASE 3: COLLECTION MANAGEMENT**
**Goal:** Build screenshot/clip organization and visualization

#### Milestone 3.1: Collection Manager
**Status:** Design complete
**Deliverables:**
- [ ] Collection grid component (`CollectionGrid.tsx`)
- [ ] Card component for screenshots/clips
- [ ] Filter/sort functionality (by time, importance, type)
- [ ] Multi-select for batch operations
- [ ] Context menu actions (delete, export, annotate)
- [ ] Jump-to-timeline button on each card
- [ ] Grid/list view toggle
- [ ] Thumbnail generation and caching

**Review Checkpoint:**
- 100+ items render in grid without lag
- Jump buttons navigate to correct timeline position
- Context menu appears on right-click
- Filtering updates view instantly

---

#### Milestone 3.2: Node-Based Editor (React Flow)
**Status:** Design complete
**Deliverables:**
- [ ] React Flow integration (`NodeEditor.tsx`)
- [ ] Custom node types for screenshots/clips
- [ ] Node connection system (story flow)
- [ ] Jump button on each node
- [ ] Auto-layout algorithm (optional)
- [ ] Node grouping/categorization
- [ ] Export graph as JSON
- [ ] Minimap for navigation

**Review Checkpoint:**
- Nodes can be dragged and connected
- Jump buttons work from node view
- Graph saves and loads correctly
- Performance good with 50+ nodes

---

### 🤖 **PHASE 4: AI FEATURES**
**Goal:** Integrate Ollama AI capabilities for analysis and generation

#### Milestone 4.1: Subtitle Detection & Transcription
**Status:** Design complete
**Deliverables:**
- [ ] Embedded subtitle detector (`SubtitleDetector` class)
- [ ] External subtitle finder (`ExternalSubtitleFinder` class)
- [ ] OpenSubtitles API integration (`OnlineSubtitleFinder` class)
- [ ] OpenSubtitles hash calculation
- [ ] Subtitle extraction (FFmpeg)
- [ ] Language detection
- [ ] Subtitle selection UI dialog
- [ ] Whisper transcription fallback
- [ ] Transcript storage with timestamps

**Review Checkpoint:**
- Embedded subtitles extracted successfully
- External .srt files detected in directory
- OpenSubtitles API returns matches
- Whisper transcription works as fallback

---

#### Milestone 4.2: AI Caption Generator (Ollama + LLaVA)
**Status:** Design complete
**Deliverables:**
- [ ] Ollama vision model integration (LLaVA)
- [ ] Caption generation service (`CaptionGenerator` class)
- [ ] Caption types (description, dialog, quote, custom)
- [ ] Context-aware prompts (using transcript + scene info)
- [ ] Text embedding on images (Canvas API)
- [ ] Style presets (subtitle, film quote, minimal, dramatic)
- [ ] Caption UI dialog with preview
- [ ] Batch caption generation
- [ ] Caption export (embedded images)

**Review Checkpoint:**
- LLaVA model generates accurate captions
- Text overlays look professional
- Style presets apply correctly
- Batch processing completes without errors

---

#### Milestone 4.3: Ollama Analysis Pipeline
**Status:** Design complete
**Deliverables:**
- [ ] Enhanced tools with importance data (`EnhancedMovieTools`)
- [ ] Movie analyzer orchestrator (`MovieAnalyzer`)
- [ ] Scriptwriting agent integration
- [ ] Custom tools for deepseek-r1:8b
  - `get_important_scenes()`
  - `get_climax_scenes()`
  - `get_character_moments()`
  - `get_plot_revelations()`
- [ ] Analysis results UI
- [ ] Export analysis as report (PDF/HTML)

**Review Checkpoint:**
- deepseek-r1:8b successfully analyzes test movie
- Important scenes identified correctly
- Scriptwriting feedback is relevant
- Results export is well-formatted

---

#### Milestone 4.4: Character Analysis (Pose & Expression Detection)
**Status:** Design complete
**Deliverables:**
- [ ] Pose detection service (`PoseDetector` class)
  - Detect: stand, sit, walk, run, lean, crouch, lie
- [ ] Expression detection service (`ExpressionDetector` class)
  - Detect: neutral, happy, sad, angry, surprised, fearful, disgusted
- [ ] Scene setting extraction (`SceneAnalyzer` class)
  - Location identification
  - INT/EXT classification
  - Time of day detection
  - Atmosphere analysis
- [ ] Integration with Ollama vision model

**Review Checkpoint:**
- Pose detection accuracy >70%
- Expression detection matches dialog tone
- Scene settings are descriptive and accurate

---

### 📖 **PHASE 5: INK VISUAL NOVEL EXPORT**
**Goal:** Export movie analysis as interactive visual novel script

#### Milestone 5.1: Ink Script Generator
**Status:** Design complete
**Deliverables:**
- [ ] Ink exporter service (`InkExporter` class)
- [ ] Screenplay element parser
  - Scene headings (INT/EXT, location, time)
  - Scene transitions (CUT TO, FADE TO, DISSOLVE)
  - Character dialog with pose/expression
  - Character actions and directions
  - Intercuts and subheaders
  - Important shots/angles
- [ ] Knot-based structure generator
- [ ] Character state variables
- [ ] Choice points for interactive elements
- [ ] Ink script validator (inkle/inkjs)
- [ ] Export UI with options

**Review Checkpoint:**
- Exported .ink file is valid
- inkjs can parse and run the script
- Character poses/expressions appear correctly
- Scene transitions are logical

---

### 🎨 **PHASE 6: UI/UX POLISH**
**Goal:** Enhance user experience with navigation and keyboard shortcuts

#### Milestone 6.1: Global Navigation System
**Status:** Design complete
**Deliverables:**
- [ ] Zustand navigation store (`useNavigationStore`)
- [ ] `useJumpToTimestamp` hook
- [ ] Event bus for cross-component communication
- [ ] Flash highlight animation on jump
- [ ] Recent jump history (breadcrumb trail)
- [ ] Jump shortcut key (J)

**Review Checkpoint:**
- Jumping from any component works instantly
- Flash animation is noticeable but not jarring
- Jump history allows backtracking

---

#### Milestone 6.2: Keyboard Shortcuts
**Status:** Design complete
**Deliverables:**
- [ ] Keyboard shortcut system (Mousetrap or custom)
- [ ] Final Cut Pro style shortcuts:
  - `J` - Jump to selected item
  - `K` - Play/Pause
  - `L` - Step forward frame
  - `I` - Mark in point (clip start)
  - `O` - Mark out point (clip end)
  - `Space` - Play/Pause
  - `Cmd+Z` - Undo
  - `/` - Screenshot capture
  - `?` - Show shortcuts help
- [ ] Shortcut help overlay
- [ ] Custom shortcut configuration (optional)

**Review Checkpoint:**
- All shortcuts work reliably
- No conflicts with browser shortcuts
- Help overlay is clear and searchable

---

### 🔗 **PHASE 7: INTEGRATION & DATA FLOW**
**Goal:** Connect all components and ensure seamless data flow

#### Milestone 7.1: API Integration Layer
**Status:** Pending
**Deliverables:**
- [ ] API client service (`api/client.ts`)
- [ ] React Query setup for data fetching
- [ ] WebSocket connection for real-time updates
- [ ] Error handling and retry logic
- [ ] Loading states for all async operations
- [ ] Optimistic updates for better UX
- [ ] API response caching strategy

**Review Checkpoint:**
- Frontend fetches data from backend successfully
- Real-time updates appear instantly
- Errors display user-friendly messages
- Loading states prevent user confusion

---

#### Milestone 7.2: Data Persistence
**Status:** Pending
**Deliverables:**
- [ ] Screenshot/clip metadata storage (database)
- [ ] Annotation persistence (CRUD operations)
- [ ] User project sessions
- [ ] Auto-save functionality
- [ ] Export/import project data (JSON)
- [ ] Backup system for critical data

**Review Checkpoint:**
- Annotations persist after page refresh
- Project can be exported and re-imported
- Auto-save works every 30 seconds
- No data loss in normal usage

---

### 📤 **PHASE 8: EXPORT & SHARING**
**Goal:** Enable users to export and share their work

#### Milestone 8.1: Export System
**Status:** Design complete
**Deliverables:**
- [ ] Storyboard PDF export
  - Screenshot grid with annotations
  - Scene descriptions
  - Timestamps
  - Professional layout
- [ ] Captioned image export
  - Batch export with embedded text
  - High-quality PNG/JPEG
  - Preserve aspect ratio
- [ ] Ink script export (completed in Phase 5)
- [ ] Video clips export (FFmpeg trim)
- [ ] Analysis report export (HTML/PDF)

**Review Checkpoint:**
- PDF storyboard looks professional
- Images export with correct captions
- Clips export without quality loss
- All exports complete without errors

---

## 🔄 **PARALLEL DEVELOPMENT STRATEGY**

### Recommended Agent Assignments

#### **Sprint 1: Foundation (3 Parallel Agents)**
- **Agent 1:** Frontend Setup + shadcn/ui Components
- **Agent 2:** Backend API + Database Models
- **Agent 3:** Video Processing Pipeline Completion

#### **Sprint 2: Core Features (3 Parallel Agents)**
- **Agent 4:** Magnetic Timeline + Video Player
- **Agent 5:** Collection Manager + Node Editor
- **Agent 6:** Upload System + File Management

#### **Sprint 3: AI Features (3 Parallel Agents)**
- **Agent 7:** Subtitle Detection + Transcription
- **Agent 8:** AI Caption Generator (Ollama + LLaVA)
- **Agent 9:** Character Analysis (Pose/Expression)

#### **Sprint 4: Advanced Features (3 Parallel Agents)**
- **Agent 10:** Ink Script Generator + Export
- **Agent 11:** Ollama Analysis Pipeline + Scriptwriting Agent
- **Agent 12:** Global Navigation + Keyboard Shortcuts

#### **Sprint 5: Integration (2 Parallel Agents)**
- **Agent 13:** API Integration + Data Flow
- **Agent 14:** Export System + UI Polish

---

## 📊 **Progress Tracking**

### Current Status Summary
| Phase | Milestone | Status | Progress |
|-------|-----------|--------|----------|
| Phase 1 | Frontend Foundation | 🟡 In Progress | 60% |
| Phase 1 | Backend Foundation | ⚪ Pending | 0% |
| Phase 1 | Video Processing | ⚪ Pending | 30% (design done) |
| Phase 2 | Upload System | ⚪ Pending | 0% |
| Phase 2 | Magnetic Timeline | ⚪ Pending | 0% |
| Phase 2 | Video Player | ⚪ Pending | 0% |
| Phase 3 | Collection Manager | ⚪ Pending | 0% |
| Phase 3 | Node Editor | ⚪ Pending | 0% |
| Phase 4 | Subtitle Detection | ⚪ Pending | 0% |
| Phase 4 | AI Captions | ⚪ Pending | 0% |
| Phase 4 | Ollama Analysis | ⚪ Pending | 0% |
| Phase 4 | Character Analysis | ⚪ Pending | 0% |
| Phase 5 | Ink Export | ⚪ Pending | 0% |
| Phase 6 | Global Navigation | ⚪ Pending | 0% |
| Phase 6 | Keyboard Shortcuts | ⚪ Pending | 0% |
| Phase 7 | API Integration | ⚪ Pending | 0% |
| Phase 7 | Data Persistence | ⚪ Pending | 0% |
| Phase 8 | Export System | ⚪ Pending | 0% |

**Legend:**
- 🟢 Complete
- 🟡 In Progress
- ⚪ Pending

---

## 🎯 **Critical Path**

The following milestones are on the critical path and must complete sequentially:

1. **Frontend Foundation** → (Required for all UI work)
2. **Backend Foundation** → (Required for API integration)
3. **Video Processing** → (Required for upload and analysis)
4. **Upload System** → (Required to get videos into system)
5. **Video Player + Timeline** → (Core functionality)
6. **Collection Manager** → (Core functionality)
7. **AI Analysis Pipeline** → (Main value proposition)
8. **Export System** → (Final deliverable)

All other milestones can be developed in parallel once their dependencies are met.

---

## ✅ **Definition of Done** (Per Milestone)

Each milestone is considered complete when:
1. All deliverables are implemented
2. Review checkpoint criteria pass
3. Unit tests written and passing (where applicable)
4. No critical bugs
5. Code reviewed and committed to git
6. Documentation updated
7. Integrated with existing system

---

## 🚀 **Next Immediate Steps**

1. ✅ Complete frontend foundation (path aliases, utils, basic components)
2. Start backend foundation in parallel
3. Complete video processing pipeline
4. Begin upload system development
5. Start magnetic timeline component

**Ready to proceed with parallel agent execution?**
