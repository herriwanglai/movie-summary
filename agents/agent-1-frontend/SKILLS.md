# Agent 1: Frontend Components & UI

## Role
Frontend developer building METEORA LX user interface with React, TypeScript, and shadcn/ui.

## Primary Responsibility
Build core React components and UI features for the video upload MVP, focusing on user experience and dark mode aesthetics.

## Tech Stack
- **Framework:** React 19 + TypeScript
- **Build Tool:** Vite
- **UI Library:** shadcn/ui (Radix UI + Tailwind CSS v4)
- **Styling:** Tailwind CSS v4 with dark mode
- **State Management:** Zustand
- **Routing:** React Router (if needed)
- **Video Player:** Plyr or video.js
- **HTTP Client:** fetch API or axios

## Documentation Sub-Agent Responsibilities

### **Priority 1: React 19 & TypeScript Best Practices**
- Learn React 19 new features (especially Server Components awareness)
- Study TypeScript best practices with React hooks
- Understand proper component composition patterns
- Learn error boundary best practices
- Study React 19 performance optimization (useMemo, useCallback)

### **Priority 2: shadcn/ui Component Patterns**
- How to install shadcn/ui components via CLI
- Study Button, Card, Progress, Dialog, Input components
- Learn proper component customization with variants
- Understand Radix UI primitives usage
- Study accessibility patterns in shadcn/ui

### **Priority 3: Tailwind CSS v4 Syntax**
- Learn @theme directive for color configuration
- Understand CSS variable usage in Tailwind v4
- Study responsive design utilities
- Learn custom animation patterns
- Understand dark mode implementation

### **Priority 4: File Upload UI Patterns**
- Study drag-and-drop file upload implementations
- Learn chunked upload progress tracking
- Understand resumable upload UI patterns
- Study error handling for file uploads
- Learn file type validation UI

### **Priority 5: Video Player Integration**
- Research Plyr vs video.js comparison
- Learn video.js API and event system
- Study custom controls implementation
- Understand video loading states
- Learn fullscreen API usage

## Key Implementation Tasks

### **Task 1: shadcn/ui Setup** (30 min)
```bash
# Install shadcn/ui components
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add progress
npx shadcn@latest add dialog
npx shadcn@latest add input
npx shadcn@latest add badge
npx shadcn@latest add toast
```

**Deliverables:**
- All components installed in `src/components/ui/`
- Components render correctly with dark theme
- Test each component in isolation

---

### **Task 2: Upload UI Component** (1-2 hours)

**File:** `src/components/upload/VideoUploader.tsx`

**Features:**
- Drag-and-drop zone with visual feedback
- File picker button (fallback)
- File type validation (mp4, mkv, avi, mov, webm)
- File size display
- Upload progress bar (chunked)
- Pause/resume buttons
- Cancel upload button
- Error messages with retry

**Required Sub-Components:**
- `DropZone.tsx` - Drag-and-drop area
- `UploadProgress.tsx` - Progress indicator
- `FileInfo.tsx` - File metadata display

**Zustand Store:** `src/stores/uploadStore.ts`
```typescript
interface UploadState {
  file: File | null
  progress: number
  status: 'idle' | 'uploading' | 'paused' | 'completed' | 'error'
  uploadId: string | null
  chunksUploaded: number[]
  error: string | null

  setFile: (file: File) => void
  startUpload: () => Promise<void>
  pauseUpload: () => void
  resumeUpload: () => void
  cancelUpload: () => void
}
```

**API Integration:**
```typescript
// src/api/upload.ts
async function initUpload(file: File): Promise<{ uploadId: string }>
async function uploadChunk(uploadId: string, chunk: Blob, index: number): Promise<void>
async function completeUpload(uploadId: string): Promise<{ videoId: string }>
```

**Success Criteria:**
- Can select video file via drag-drop or picker
- Shows file name, size, duration (if extractable)
- Upload progress updates in real-time
- Can pause and resume upload
- Error handling with clear messages

---

### **Task 3: Video Player Component** (2-3 hours)

**File:** `src/components/player/VideoPlayer.tsx`

**Features:**
- Video playback with custom controls
- Play/pause button
- Timeline scrubber
- Volume control
- Fullscreen toggle
- Playback speed control (0.5x, 1x, 1.5x, 2x)
- Current time / duration display
- Loading state skeleton

**Optional Features:**
- Thumbnail preview on hover
- Keyboard shortcuts (Space for play/pause)
- Double-click for fullscreen

**Props Interface:**
```typescript
interface VideoPlayerProps {
  videoId?: string
  src?: string
  onTimeUpdate?: (currentTime: number) => void
  onReady?: () => void
  className?: string
}
```

**Success Criteria:**
- Video plays uploaded files
- Controls are responsive and intuitive
- Fullscreen works correctly
- Loading states prevent UI jank
- Dark theme styling matches METEORA LX

---

### **Task 4: State Management Setup** (1 hour)

**File:** `src/stores/index.ts`

**Stores to Create:**
- `uploadStore.ts` - Upload state and actions
- `videoStore.ts` - Current video data
- `playerStore.ts` - Player state (time, playing, volume)

**Example Zustand Store:**
```typescript
import { create } from 'zustand'

interface VideoStore {
  currentVideo: Video | null
  scenes: Scene[]
  keyframes: Keyframe[]

  setCurrentVideo: (video: Video) => void
  loadScenes: (videoId: string) => Promise<void>
}

export const useVideoStore = create<VideoStore>((set) => ({
  currentVideo: null,
  scenes: [],
  keyframes: [],

  setCurrentVideo: (video) => set({ currentVideo: video }),
  loadScenes: async (videoId) => {
    const scenes = await fetchScenes(videoId)
    set({ scenes })
  },
}))
```

**Success Criteria:**
- State updates trigger re-renders
- No prop drilling required
- State persists across component unmounts (where needed)

---

### **Task 5: Error Boundaries & Loading States** (1 hour)

**File:** `src/components/ErrorBoundary.tsx`

**Features:**
- Catch React errors gracefully
- Display user-friendly error messages
- Provide retry mechanism
- Log errors to console (dev) or service (prod)

**File:** `src/components/LoadingStates.tsx`

**Components:**
- `VideoPlayerSkeleton` - Player loading state
- `UploadSkeleton` - Upload UI loading state
- `Spinner` - General loading spinner

**Success Criteria:**
- Errors don't crash the app
- Loading states show during async operations
- User knows what's happening at all times

---

## Integration Points

### **With Agent 2 (Backend API):**
- **API Endpoints to Call:**
  - `POST /api/upload/init`
  - `POST /api/upload/chunk`
  - `POST /api/upload/complete`
  - `GET /api/videos`
  - `GET /api/videos/{videoId}`
  - `GET /api/videos/{videoId}/stream`

- **Expected Request/Response:**
```typescript
// Init Upload
POST /api/upload/init
Body: { filename: string, fileSize: number, mimeType: string }
Response: { uploadId: string, chunkSize: number }

// Upload Chunk
POST /api/upload/chunk
Body: FormData with chunk blob
Response: { chunkIndex: number, progress: number }

// Complete Upload
POST /api/upload/complete
Body: { uploadId: string }
Response: { videoId: string, status: string }
```

### **With Agent 3 (Video Processing):**
- **Display Processing Status:**
  - Listen for processing events (WebSocket or polling)
  - Show "Processing..." state in UI
  - Display scenes/keyframes when ready

## Testing Checklist

- [ ] Can drag-drop video file onto upload zone
- [ ] Can select video via file picker
- [ ] Upload progress bar updates correctly
- [ ] Can pause and resume upload
- [ ] Upload completes successfully
- [ ] Video player loads uploaded video
- [ ] Player controls work (play, pause, seek, volume)
- [ ] Fullscreen works
- [ ] Error messages display on failure
- [ ] Loading states show during async operations
- [ ] Dark theme renders correctly
- [ ] Responsive on mobile and desktop

## Documentation Sub-Agent Deliverables

Before starting implementation, the sub-agent should provide:

1. **React 19 Cheat Sheet:**
   - Best practices for hooks
   - TypeScript patterns
   - Performance tips

2. **shadcn/ui Guide:**
   - Installation commands
   - Component customization examples
   - Variant patterns

3. **Tailwind v4 Reference:**
   - @theme syntax examples
   - Dark mode utilities
   - Custom animation setup

4. **File Upload Best Practices:**
   - Chunked upload implementation
   - Progress tracking
   - Error handling patterns

5. **Video Player Integration Guide:**
   - Recommended library (Plyr or video.js)
   - Basic setup code
   - Custom controls example

## Success Criteria

Agent 1 is complete when:
1. ✅ All shadcn/ui components installed and working
2. ✅ Video upload UI functional with drag-drop
3. ✅ Progress bar shows real upload progress
4. ✅ Video player displays uploaded videos
5. ✅ State management working with Zustand
6. ✅ Error boundaries catch failures
7. ✅ Loading states prevent UI confusion
8. ✅ Dark theme consistent across all components
9. ✅ No TypeScript errors
10. ✅ Code committed with clear messages

## Estimated Timeline
- shadcn/ui setup: **30 min**
- Upload UI: **1-2 hours**
- Video player: **2-3 hours**
- State management: **1 hour**
- Error handling: **1 hour**
- Testing & refinement: **1 hour**

**Total: 6.5-8.5 hours**

## Notes for Agent
- Prioritize MVP functionality over polish
- Focus on dark mode aesthetics (cinematic feel)
- Use TypeScript strictly (no `any` types)
- Follow shadcn/ui patterns for consistency
- Document complex logic with comments
- Keep components small and focused
- Test upload with large files (1GB+)
