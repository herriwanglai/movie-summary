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
- **Video Player:** Vidstack (modern, TypeScript-first)
- **Upload Client:** Uppy with TUS plugin
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

### **Priority 4: TUS Upload with Uppy**
- Learn Uppy file uploader library
- Study TUS (resumable upload) plugin
- Understand drag-and-drop with Uppy Dashboard
- Learn progress tracking with Uppy
- Study error handling and retry mechanisms
- Learn Uppy React hooks and components

### **Priority 5: Vidstack Player Integration**
- Learn Vidstack React library (@vidstack/react)
- Study MediaPlayer and MediaProvider components
- Understand Vidstack screenshot/thumbnail API
- Learn custom controls and layouts
- Study keyboard shortcuts integration
- Learn dark mode theming with Vidstack

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

### **Task 2: TUS Upload with Uppy** (30 minutes) ⚡

**Using Uppy + TUS plugin - production-ready upload solution!**

**Installation:**
```bash
npm install @uppy/core @uppy/react @uppy/tus @uppy/dashboard @uppy/drag-drop
```

**File:** `src/components/upload/VideoUploader.tsx`

```typescript
import Uppy from '@uppy/core'
import Tus from '@uppy/tus'
import { Dashboard } from '@uppy/react'
import { useEffect, useState } from 'react'

import '@uppy/core/dist/style.min.css'
import '@uppy/dashboard/dist/style.min.css'

function VideoUploader() {
  const [uppy] = useState(() =>
    new Uppy({
      restrictions: {
        maxFileSize: 10 * 1024 * 1024 * 1024, // 10GB
        allowedFileTypes: ['video/*'],
      },
      autoProceed: false,
    })
      .use(Tus, {
        endpoint: 'http://localhost:8000/api/upload/',
        chunkSize: 5 * 1024 * 1024, // 5MB chunks
        retryDelays: [0, 1000, 3000, 5000],
      })
  )

  useEffect(() => {
    uppy.on('complete', (result) => {
      console.log('Upload complete!', result.successful)
      // Navigate to video page or trigger processing
    })

    uppy.on('error', (error) => {
      console.error('Upload error:', error)
    })

    return () => uppy.close()
  }, [uppy])

  return (
    <div className="w-full max-w-4xl mx-auto">
      <Dashboard
        uppy={uppy}
        proudlyDisplayPoweredByUppy={false}
        theme="dark"
        width="100%"
        height={450}
      />
    </div>
  )
}
```

**That's it!** 🎉 Uppy + TUS handles:
- ✅ Drag-and-drop UI
- ✅ File picker
- ✅ Progress tracking
- ✅ Pause/resume (TUS)
- ✅ Retry logic
- ✅ Error handling
- ✅ Multiple file queuing
- ✅ Dark theme

**Success Criteria:**
- Uppy Dashboard renders in dark mode
- Can drag-drop or select video files
- Progress bar shows upload status
- Pause/resume works automatically (TUS)
- Upload completes successfully

---

### **Task 3: Vidstack Video Player** (30-45 minutes) ⚡

**Using Vidstack - modern, TypeScript-first video player!**

**Installation:**
```bash
npm install @vidstack/react
```

**File:** `src/components/player/VideoPlayer.tsx`

```typescript
import { MediaPlayer, MediaProvider } from '@vidstack/react'
import { defaultLayoutIcons, DefaultVideoLayout } from '@vidstack/react/player/layouts/default'
import { useRef } from 'react'

import '@vidstack/react/player/styles/default/theme.css'
import '@vidstack/react/player/styles/default/layouts/video.css'

interface VideoPlayerProps {
  src: string
  title?: string
  onTimeUpdate?: (time: number) => void
  onScreenshot?: (dataUrl: string) => void
}

function VideoPlayer({ src, title, onTimeUpdate, onScreenshot }: VideoPlayerProps) {
  const playerRef = useRef<MediaPlayer>(null)

  const handleScreenshot = async () => {
    if (playerRef.current) {
      const canvas = document.createElement('canvas')
      const video = playerRef.current.el?.querySelector('video')

      if (video) {
        canvas.width = video.videoWidth
        canvas.height = video.videoHeight
        const ctx = canvas.getContext('2d')
        ctx?.drawImage(video, 0, 0)
        const dataUrl = canvas.toDataURL('image/png')
        onScreenshot?.(dataUrl)
      }
    }
  }

  return (
    <MediaPlayer
      ref={playerRef}
      src={src}
      title={title}
      className="w-full aspect-video"
      onTimeUpdate={(e) => onTimeUpdate?.(e.detail.currentTime)}
    >
      <MediaProvider />
      <DefaultVideoLayout
        icons={defaultLayoutIcons}
        thumbnails="https://media-files.vidstack.io/sprite-fight/thumbnails.vtt"
      />
    </MediaPlayer>
  )
}
```

**Built-in Features (No Extra Code!):**
- ✅ Play/pause controls
- ✅ Timeline scrubber with preview
- ✅ Volume control
- ✅ Fullscreen toggle
- ✅ Playback speed (0.25x - 2x)
- ✅ Picture-in-Picture
- ✅ Keyboard shortcuts (Space, Arrow keys, F, M, etc.)
- ✅ Loading states
- ✅ Dark mode theme
- ✅ Responsive design
- ✅ Accessibility (ARIA)
- ✅ TypeScript types

**Screenshot Functionality:**
Add a screenshot button to the player:
```typescript
import { useMediaState } from '@vidstack/react'

// In component:
const isPaused = useMediaState('paused', playerRef)

<button onClick={handleScreenshot} disabled={!isPaused}>
  Take Screenshot
</button>
```

**Success Criteria:**
- Video plays uploaded files
- All controls work out of the box
- Dark theme matches METEORA LX
- Keyboard shortcuts functional
- Screenshot feature works
- TypeScript types are correct

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

4. **Uppy + TUS Upload Guide:**
   - Uppy Dashboard setup
   - TUS plugin configuration
   - Event handling (complete, error, progress)
   - Dark theme customization

5. **Vidstack Player Guide:**
   - MediaPlayer component setup
   - Layout customization
   - Screenshot/thumbnail API
   - Event listeners and hooks
   - TypeScript types reference

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
- Upload UI (Uppy + TUS): **30 min** ⚡ (was 1-2 hours!)
- Video player (Vidstack): **30-45 min** ⚡ (was 2-3 hours!)
- State management: **1 hour**
- Error handling: **30 min** (less needed with libraries)
- Testing & refinement: **1 hour**

**Total: 4-4.5 hours** (down from 6.5-8.5 hours!)

**Time saved by using Uppy + Vidstack: 2.5-4 hours!** 🎉

## Notes for Agent
- Prioritize MVP functionality over polish
- Focus on dark mode aesthetics (cinematic feel)
- Use TypeScript strictly (no `any` types)
- Follow shadcn/ui patterns for consistency
- Document complex logic with comments
- Keep components small and focused
- Test upload with large files (1GB+)
