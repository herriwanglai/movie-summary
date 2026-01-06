# UI/UX Implementation Plan: Interactive Movie Analysis Interface

## 📋 Overview

Add a React-based web interface for interactive movie analysis with:
- **Video player** with screenshot/clip pinpointing
- **Node-based editor** for visualizing scenes and relationships
- **Interactive timeline** for scene navigation
- **Collection manager** for screenshots and clips

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React + TypeScript)            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  Video Player    │  │  Node Editor     │                │
│  │  Component       │  │  (React Flow)    │                │
│  │  - Screenshot    │  │  - Scene nodes   │                │
│  │  - Clip          │  │  - Character     │                │
│  │  - Annotations   │  │  - Connections   │                │
│  └────────┬─────────┘  └────────┬─────────┘                │
│           │                     │                           │
│  ┌────────┴─────────────────────┴─────────┐                │
│  │      Collection Manager                │                │
│  │      - Screenshots gallery             │                │
│  │      - Clips library                   │                │
│  │      - Export/Import                   │                │
│  └────────────────┬───────────────────────┘                │
│                   │                                         │
└───────────────────┼─────────────────────────────────────────┘
                    │
                    │ REST API / WebSocket
                    │
┌───────────────────┼─────────────────────────────────────────┐
│                   │     BACKEND (FastAPI + Python)          │
├───────────────────┴─────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  Video Service   │  │  Analysis Engine │                │
│  │  - Streaming     │  │  - Ollama        │                │
│  │  - Frame extract │  │  - Importance    │                │
│  │  - Clip generate │  │  - Transcription │                │
│  └──────────────────┘  └──────────────────┘                │
│                                                              │
│  ┌──────────────────────────────────────────┐              │
│  │  Annotation Storage                      │              │
│  │  - SQLite / PostgreSQL                   │              │
│  │  - Screenshots metadata                  │              │
│  │  - Clips metadata                        │              │
│  │  - Node graph data                       │              │
│  └──────────────────────────────────────────┘              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎯 Core Components

### 1. Video Player Component

**Technology:** React + video.js or Plyr

**Features:**
- ▶️ Standard playback controls (play, pause, seek, volume)
- 📸 Screenshot button - capture current frame
- ✂️ Clip mode - mark start/end points for clips
- 🏷️ Annotation mode - add notes at timestamps
- ⏱️ Frame-by-frame navigation (← → keys)
- 🎨 Drawing tools for annotations on frames

**Logic:**
```typescript
interface VideoPlayer {
  // State
  currentTime: number;
  duration: number;
  isPlaying: boolean;
  clipMarkers: { start: number; end: number }[];
  screenshots: Screenshot[];

  // Actions
  captureScreenshot(): Screenshot;
  startClipMarker(): void;
  endClipMarker(): Clip;
  addAnnotation(text: string, timestamp: number): void;
  seekToTimestamp(time: number): void;

  // Events
  onTimeUpdate(callback: (time: number) => void): void;
  onScreenshot(callback: (screenshot: Screenshot) => void): void;
  onClipCreated(callback: (clip: Clip) => void): void;
}

interface Screenshot {
  id: string;
  timestamp: number;
  imageUrl: string;
  thumbnailUrl: string;
  annotation?: string;
  sceneNumber?: number;
  importanceScore?: number;
}

interface Clip {
  id: string;
  startTime: number;
  endTime: number;
  duration: number;
  videoUrl: string;
  thumbnailUrl: string;
  description?: string;
  sceneNumbers: number[];
}
```

### 2. Node-Based Editor (React Flow)

**Technology:** React Flow (https://reactflow.dev/)

**Node Types:**
- 🎬 **Scene Node** - Represents a scene with thumbnail
- 👤 **Character Node** - Character with relationships
- 💬 **Dialogue Node** - Important dialogue quotes
- 📸 **Screenshot Node** - User-captured screenshots
- ✂️ **Clip Node** - Video clip segments
- 🎯 **Plot Point Node** - Story beats

**Connections:**
- Scene → Scene (sequence)
- Character → Character (relationships)
- Scene → Character (appears in)
- Dialogue → Character (spoken by)
- Screenshot/Clip → Scene (belongs to)

**Logic:**
```typescript
interface NodeEditorState {
  nodes: Node[];
  edges: Edge[];
  selectedNode: Node | null;

  // Auto-layout options
  layoutType: 'timeline' | 'hierarchy' | 'force' | 'custom';

  // Actions
  addSceneNodes(scenes: Scene[]): void;
  addCharacterNode(character: Character): void;
  addScreenshotNode(screenshot: Screenshot): void;
  addClipNode(clip: Clip): void;
  connectNodes(sourceId: string, targetId: string, type: EdgeType): void;
  autoLayout(): void;

  // Export
  exportAsJSON(): string;
  exportAsImage(): Blob;
  exportAsVideo(): Blob; // Compile clips in order
}

interface SceneNode extends Node {
  data: {
    sceneNumber: number;
    thumbnail: string;
    timestamp: [number, number]; // [start, end]
    importanceScore: number;
    description: string;
    screenshots: Screenshot[];
    clips: Clip[];
  };
}

interface CharacterNode extends Node {
  data: {
    name: string;
    avatar?: string;
    motivations: string[];
    relationships: {
      character: string;
      type: 'ally' | 'conflict' | 'romantic' | 'family';
    }[];
  };
}
```

### 3. Collection Manager

**Purpose:** Manage all screenshots and clips in one place

**Features:**
- 🖼️ Gallery view of screenshots
- 🎞️ Library view of clips
- 🔍 Search and filter
- 🏷️ Tagging system
- 📤 Export options (ZIP, JSON)
- 🔄 Sync with node editor

**Logic:**
```typescript
interface CollectionManager {
  screenshots: Screenshot[];
  clips: Clip[];
  tags: Tag[];

  // Filtering
  filterByScene(sceneNumber: number): (Screenshot | Clip)[];
  filterByTag(tag: string): (Screenshot | Clip)[];
  filterByTimeRange(start: number, end: number): (Screenshot | Clip)[];

  // Organization
  addTag(itemId: string, tag: string): void;
  bulkExport(items: string[]): Blob;

  // Actions
  deleteItem(id: string): void;
  editAnnotation(id: string, annotation: string): void;
  linkToNode(itemId: string, nodeId: string): void;
}
```

### 4. Interactive Timeline

**Purpose:** Visual timeline of scenes with annotations

**Features:**
- 📊 Scene blocks with importance color coding
- 📍 Screenshot/clip markers
- 🎭 Character appearance tracks
- 📈 Emotional intensity graph
- 🖱️ Click to seek in video

**Logic:**
```typescript
interface Timeline {
  duration: number;
  scenes: SceneBlock[];
  markers: TimelineMarker[];
  tracks: Track[];

  // Visualization
  renderScenes(): SceneBlock[];
  renderMarkers(): TimelineMarker[];
  renderIntensityGraph(): number[];

  // Interaction
  onMarkerClick(marker: TimelineMarker): void;
  onSceneClick(scene: SceneBlock): void;
  addMarker(timestamp: number, type: MarkerType): void;
}

interface SceneBlock {
  sceneNumber: number;
  startTime: number;
  endTime: number;
  importanceScore: number;
  color: string; // Based on importance
  hasScreenshots: boolean;
  hasClips: boolean;
}

interface TimelineMarker {
  id: string;
  timestamp: number;
  type: 'screenshot' | 'clip_start' | 'clip_end' | 'annotation';
  label?: string;
  color: string;
}
```

---

## 🔌 Backend API Endpoints

### Video Service

```python
# FastAPI Endpoints

# Stream video
GET /api/video/{video_id}/stream
  → Returns: Video stream with range support

# Get frame at timestamp
GET /api/video/{video_id}/frame?timestamp={seconds}
  → Returns: Image (JPEG)

# Extract clip
POST /api/video/{video_id}/clip
  Body: { start: number, end: number }
  → Returns: { clipUrl: string, thumbnailUrl: string }

# Get video metadata
GET /api/video/{video_id}/metadata
  → Returns: { duration, fps, resolution, scenes[], transcript }
```

### Annotation Service

```python
# Save screenshot annotation
POST /api/annotations/screenshot
  Body: Screenshot
  → Returns: { id: string }

# Save clip annotation
POST /api/annotations/clip
  Body: Clip
  → Returns: { id: string }

# Get all annotations
GET /api/annotations/{video_id}
  → Returns: { screenshots: [], clips: [] }

# Update annotation
PATCH /api/annotations/{id}
  Body: { annotation: string, tags: string[] }
  → Returns: { success: boolean }

# Delete annotation
DELETE /api/annotations/{id}
  → Returns: { success: boolean }
```

### Node Graph Service

```python
# Save node graph
POST /api/graph/{video_id}
  Body: { nodes: [], edges: [] }
  → Returns: { id: string }

# Load node graph
GET /api/graph/{video_id}
  → Returns: { nodes: [], edges: [] }

# Auto-generate graph from analysis
POST /api/graph/{video_id}/auto-generate
  → Returns: { nodes: [], edges: [] }
  # Uses importance detection + character analysis
```

---

## 💾 Data Models

### Database Schema (SQLite/PostgreSQL)

```sql
-- Videos
CREATE TABLE videos (
  id UUID PRIMARY KEY,
  filename VARCHAR(255),
  path VARCHAR(512),
  duration FLOAT,
  fps FLOAT,
  created_at TIMESTAMP,
  analyzed BOOLEAN DEFAULT FALSE
);

-- Scenes (from analysis)
CREATE TABLE scenes (
  id UUID PRIMARY KEY,
  video_id UUID REFERENCES videos(id),
  scene_number INTEGER,
  start_time FLOAT,
  end_time FLOAT,
  importance_score FLOAT,
  categories JSON, -- ['action', 'exciting']
  thumbnail_url VARCHAR(512)
);

-- Screenshots (user-captured)
CREATE TABLE screenshots (
  id UUID PRIMARY KEY,
  video_id UUID REFERENCES videos(id),
  scene_id UUID REFERENCES scenes(id),
  timestamp FLOAT,
  image_url VARCHAR(512),
  thumbnail_url VARCHAR(512),
  annotation TEXT,
  tags JSON,
  created_at TIMESTAMP
);

-- Clips (user-created)
CREATE TABLE clips (
  id UUID PRIMARY KEY,
  video_id UUID REFERENCES videos(id),
  start_time FLOAT,
  end_time FLOAT,
  video_url VARCHAR(512),
  thumbnail_url VARCHAR(512),
  description TEXT,
  tags JSON,
  created_at TIMESTAMP
);

-- Node graphs
CREATE TABLE node_graphs (
  id UUID PRIMARY KEY,
  video_id UUID REFERENCES videos(id),
  graph_data JSON, -- { nodes: [], edges: [] }
  layout_type VARCHAR(50),
  updated_at TIMESTAMP
);

-- Annotations (timestamps with notes)
CREATE TABLE annotations (
  id UUID PRIMARY KEY,
  video_id UUID REFERENCES videos(id),
  timestamp FLOAT,
  text TEXT,
  created_at TIMESTAMP
);
```

---

## 🎨 UI Component Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── VideoPlayer/
│   │   │   ├── VideoPlayer.tsx           # Main video component
│   │   │   ├── VideoControls.tsx         # Play/pause/seek
│   │   │   ├── ScreenshotButton.tsx      # Capture screenshot
│   │   │   ├── ClipMarker.tsx            # Mark clip boundaries
│   │   │   ├── AnnotationOverlay.tsx     # Drawing/notes
│   │   │   └── Timeline.tsx              # Video timeline
│   │   │
│   │   ├── NodeEditor/
│   │   │   ├── NodeEditor.tsx            # React Flow wrapper
│   │   │   ├── nodes/
│   │   │   │   ├── SceneNode.tsx
│   │   │   │   ├── CharacterNode.tsx
│   │   │   │   ├── ScreenshotNode.tsx
│   │   │   │   └── ClipNode.tsx
│   │   │   ├── edges/
│   │   │   │   └── CustomEdge.tsx
│   │   │   └── AutoLayout.tsx            # Auto-arrange nodes
│   │   │
│   │   ├── CollectionManager/
│   │   │   ├── CollectionManager.tsx     # Main manager
│   │   │   ├── ScreenshotGallery.tsx     # Grid view
│   │   │   ├── ClipLibrary.tsx           # Clip list
│   │   │   ├── FilterBar.tsx             # Search/filter
│   │   │   └── ExportDialog.tsx          # Export options
│   │   │
│   │   ├── InteractiveTimeline/
│   │   │   ├── Timeline.tsx              # Main timeline
│   │   │   ├── SceneBlock.tsx            # Scene representation
│   │   │   ├── Marker.tsx                # Timeline markers
│   │   │   └── IntensityGraph.tsx        # Emotion curve
│   │   │
│   │   └── Sidebar/
│   │       ├── AnalysisPanel.tsx         # AI analysis results
│   │       ├── SceneList.tsx             # Scene navigation
│   │       └── CharacterPanel.tsx        # Character info
│   │
│   ├── hooks/
│   │   ├── useVideoPlayer.ts             # Video player state
│   │   ├── useScreenshots.ts             # Screenshot management
│   │   ├── useClips.ts                   # Clip management
│   │   ├── useNodeGraph.ts               # Node editor state
│   │   └── useAnalysis.ts                # Fetch analysis data
│   │
│   ├── services/
│   │   ├── api.ts                        # API client
│   │   ├── videoService.ts               # Video operations
│   │   ├── annotationService.ts          # CRUD annotations
│   │   └── graphService.ts               # Node graph ops
│   │
│   ├── types/
│   │   ├── video.ts
│   │   ├── annotation.ts
│   │   ├── node.ts
│   │   └── analysis.ts
│   │
│   └── utils/
│       ├── timeFormat.ts                 # Time formatting
│       ├── thumbnailGenerator.ts         # Generate thumbs
│       └── exportHelpers.ts              # Export utilities
│
├── package.json
└── vite.config.ts
```

---

## 🔄 User Workflows

### Workflow 1: Capture and Organize Screenshots

```
1. User watches video in player
2. User sees interesting frame → clicks 📸 button
3. Screenshot captured and added to collection
4. User adds annotation/tags
5. Screenshot appears in:
   - Collection Manager gallery
   - Timeline as marker
   - Available as node in Node Editor
```

### Workflow 2: Create and Analyze Clips

```
1. User enables clip mode
2. User marks start point (click ✂️)
3. User plays to end point, marks end
4. Clip is generated on backend
5. Clip appears in:
   - Collection Manager library
   - Timeline as range marker
   - Available as node in Node Editor
```

### Workflow 3: Build Visual Story Map

```
1. User clicks "Auto-generate graph" button
2. Backend creates nodes for:
   - All scenes (from analysis)
   - Important moments (high importance score)
   - Characters (from character analysis)
3. User adds custom nodes:
   - Screenshot nodes
   - Clip nodes
   - Custom annotations
4. User connects nodes to show:
   - Scene sequence
   - Character relationships
   - Story beats
5. User exports as image/JSON
```

### Workflow 4: Analyze with AI Assistance

```
1. User uploads video
2. Backend runs analysis (scenes, transcript, importance)
3. UI shows:
   - Timeline with importance-colored scenes
   - Suggested "important moments" to review
   - Character relationship graph
4. User reviews important scenes
5. User captures screenshots of key moments
6. User builds custom story map
7. User exports analysis + annotations
```

---

## 📦 Technology Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Flow** - Node-based editor
- **video.js / Plyr** - Video player
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **React Query** - Data fetching
- **Framer Motion** - Animations

### Backend
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **SQLite / PostgreSQL** - Database
- **FFmpeg** - Video processing
- **Pillow** - Image processing
- **WebSocket** - Real-time updates

---

## 🚀 Implementation Phases

### Phase 1: Foundation (2-3 days)
1. Set up React project with TypeScript + Vite
2. Set up FastAPI backend with video streaming
3. Create basic video player component
4. Implement screenshot capture

### Phase 2: Core Features (3-4 days)
5. Add clip marking and generation
6. Build collection manager with gallery
7. Implement annotation storage (SQLite)
8. Create interactive timeline

### Phase 3: Node Editor (3-4 days)
9. Integrate React Flow
10. Create custom node types
11. Auto-generate graph from analysis
12. Add export functionality

### Phase 4: Integration (2-3 days)
13. Connect to existing analysis pipeline
14. Add AI-suggested important moments
15. Character relationship visualization
16. Polish and optimization

---

## ⚙️ Configuration

```yaml
# config.yaml
frontend:
  video_player:
    screenshot_quality: 95  # JPEG quality
    thumbnail_size: [320, 180]
    clip_max_duration: 300  # 5 minutes

  node_editor:
    auto_layout: 'timeline'  # timeline, hierarchy, force
    default_zoom: 1.0
    enable_minimap: true

  timeline:
    height: 120  # pixels
    zoom_levels: [1, 2, 5, 10]  # seconds per pixel
    show_intensity_graph: true

backend:
  video:
    streaming_chunk_size: 1048576  # 1MB
    supported_formats: ['.mp4', '.mkv', '.avi', '.mov']
    max_file_size: 10737418240  # 10GB

  storage:
    screenshots_dir: './output/screenshots'
    clips_dir: './output/clips'
    thumbnails_dir: './output/thumbnails'

  processing:
    ffmpeg_threads: 4
    screenshot_format: 'jpg'
    clip_codec: 'h264'
```

---

## 📊 Summary

### What We're Building:
1. **Interactive Video Player** - Watch, screenshot, clip, annotate
2. **Node-Based Editor** - Visualize scenes, characters, story structure
3. **Collection Manager** - Organize screenshots and clips
4. **Smart Timeline** - Navigate with importance-based visualization
5. **Full Integration** - Connect with existing AI analysis

### Key Technologies:
- React + TypeScript + Vite (Frontend)
- React Flow (Node editor)
- FastAPI + SQLite (Backend)
- FFmpeg (Video processing)

### User Benefits:
✅ Visual, interactive movie analysis
✅ Easy screenshot and clip capture
✅ Node-based story mapping
✅ AI-assisted important moment detection
✅ Export annotations and diagrams
✅ Collaborative analysis potential

**Ready to implement? Waiting for your confirmation to proceed!**
