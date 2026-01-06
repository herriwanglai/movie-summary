# Phase 2: Timeline & Navigation Implementation Plan

## 🎯 Overview

Implement a Final Cut Pro-style magnetic timeline with scene-based navigation and keyboard shortcuts.

---

## 📋 Features to Implement

### 1. Magnetic Timeline Component
**Visual Features:**
- Horizontal timeline spanning video duration
- Scene boundaries marked with vertical lines
- Keyframe markers within scenes
- Playhead showing current time
- Hover tooltips with timestamps
- Scene colors for visual distinction

**Interactions:**
- Click to seek to timestamp
- Drag playhead to scrub
- Hover for scene information
- Zoom in/out with scroll wheel
- Pan with drag gesture

**Data Display:**
- Scene start/end times
- Keyframe positions
- Current time indicator
- Total duration

### 2. Keyboard Shortcuts
**Playback Controls:**
- `Space` - Play/Pause
- `K` - Play/Pause (alternative)
- `J` - Rewind / Previous frame
- `L` - Fast forward / Next frame
- `←` - Previous frame (1/30s)
- `→` - Next frame (1/30s)
- `↑` - Increase volume
- `↓` - Decrease volume

**Navigation:**
- `[` - Previous scene
- `]` - Next scene
- `Home` - Jump to start
- `End` - Jump to end
- `0-9` - Jump to 0%, 10%, 20%... of video

**Timeline:**
- `+` / `=` - Zoom in
- `-` / `_` - Zoom out
- `0` - Reset zoom

### 3. Scene Navigation
**Features:**
- Previous/Next scene buttons
- Scene list sidebar
- Jump to scene by clicking
- Scene thumbnails (keyframe)
- Scene duration display
- Auto-scroll timeline to current scene

### 4. Global Navigation Bar
**Components:**
- Timeline at bottom of player
- Playback controls (play, pause, skip)
- Time display (current / total)
- Volume control
- Fullscreen toggle
- Scene markers overlay

---

## 🏗️ Component Architecture

```
App.tsx
└── VideoWorkspace.tsx (NEW)
    ├── VideoPlayer.tsx (existing)
    ├── MagneticTimeline.tsx (NEW)
    │   ├── TimelineTrack.tsx
    │   ├── SceneMarker.tsx
    │   ├── KeyframeMarker.tsx
    │   └── Playhead.tsx
    ├── PlaybackControls.tsx (NEW)
    ├── SceneNavigator.tsx (NEW)
    │   ├── SceneList.tsx
    │   └── SceneCard.tsx
    └── KeyboardShortcuts.tsx (NEW - hook)
```

---

## 📊 State Management

### Timeline Store (Zustand)
```typescript
interface TimelineState {
  // Video data
  videoId: string | null
  duration: number
  scenes: Scene[]
  keyframes: Keyframe[]

  // Playback state
  currentTime: number
  isPlaying: boolean
  playbackRate: number
  volume: number

  // Timeline state
  zoom: number
  panOffset: number
  hoveredTime: number | null
  selectedSceneId: number | null

  // Actions
  setCurrentTime: (time: number) => void
  play: () => void
  pause: () => void
  togglePlay: () => void
  nextScene: () => void
  previousScene: () => void
  jumpToScene: (sceneId: number) => void
  zoomIn: () => void
  zoomOut: () => void
  resetZoom: () => void
}
```

### Navigation Store (Zustand)
```typescript
interface NavigationState {
  shortcuts: Map<string, () => void>
  isEnabled: boolean

  registerShortcut: (key: string, action: () => void) => void
  unregisterShortcut: (key: string) => void
  enableShortcuts: () => void
  disableShortcuts: () => void
}
```

---

## 🎨 UI Design

### Color Scheme (Dark Theme)
```typescript
const colors = {
  timeline: {
    background: 'hsl(240 10% 8%)',
    track: 'hsl(240 10% 12%)',
    playhead: 'hsl(0 0% 100%)',
    scene: 'hsl(217 91% 60%)',
    sceneHover: 'hsl(217 91% 70%)',
    keyframe: 'hsl(142 76% 36%)',
    marker: 'hsl(240 5% 26%)',
  },
  controls: {
    button: 'hsl(240 10% 15%)',
    buttonHover: 'hsl(240 10% 20%)',
    buttonActive: 'hsl(217 91% 60%)',
  }
}
```

### Layout
```
┌─────────────────────────────────────────┐
│           Video Player                   │
│        (16:9 aspect ratio)              │
├─────────────────────────────────────────┤
│  Playback Controls                      │
│  [⏮] [⏪] [▶] [⏩] [⏭]  00:45 / 02:30   │
├─────────────────────────────────────────┤
│  Magnetic Timeline                      │
│  ▼─────█──────█──────█─────────────     │
│  Scene markers and keyframes            │
├─────────────────────────────────────────┤
│  Scene Navigator (collapsible)          │
│  [Scene 1] [Scene 2] [Scene 3] ...     │
└─────────────────────────────────────────┘
```

---

## 🔧 Implementation Steps

### Step 1: Timeline Store (1 hour)
- Create `stores/timelineStore.ts`
- Implement state management
- Add action creators
- Test state updates

### Step 2: Magnetic Timeline Component (2-3 hours)
- Create `MagneticTimeline.tsx`
- Render timeline track
- Add scene markers
- Add keyframe dots
- Implement playhead
- Add hover interactions
- Handle click to seek

### Step 3: Keyboard Shortcuts (1 hour)
- Create `hooks/useKeyboardShortcuts.ts`
- Register shortcuts
- Handle key events
- Prevent conflicts with inputs
- Add visual feedback

### Step 4: Scene Navigation (1-2 hours)
- Create `SceneNavigator.tsx`
- Fetch scenes from API
- Display scene list
- Add prev/next buttons
- Implement jump to scene
- Show scene thumbnails

### Step 5: Playback Controls (1 hour)
- Create `PlaybackControls.tsx`
- Add play/pause button
- Add skip buttons
- Time display
- Volume control
- Connect to timeline store

### Step 6: Timeline-Player Sync (1 hour)
- Sync video.currentTime with store
- Update playhead position
- Handle seeking
- Update on timeupdate event
- Smooth animations

### Step 7: Zoom & Pan (1 hour)
- Add wheel event for zoom
- Implement pan with drag
- Constrain zoom levels
- Update marker positions
- Smooth transitions

---

## 🧪 Testing Plan

### Unit Tests
- [ ] Timeline store actions
- [ ] Keyboard shortcut registration
- [ ] Scene navigation logic
- [ ] Time formatting utilities

### Integration Tests
- [ ] Timeline updates on video play
- [ ] Keyboard shortcuts trigger actions
- [ ] Scene navigation syncs with player
- [ ] Zoom/pan updates timeline

### Manual Tests
- [ ] Play video and watch timeline update
- [ ] Click timeline to seek
- [ ] Test all keyboard shortcuts
- [ ] Navigate through scenes
- [ ] Zoom in/out on timeline
- [ ] Test with different video lengths

---

## 📦 Dependencies

### New Libraries
```json
{
  "react-use": "^17.5.0",  // useKey, useWindowSize hooks
  "framer-motion": "^11.0.0"  // Smooth animations
}
```

### Existing Libraries
- React 19
- Zustand (state)
- Tailwind CSS (styling)
- Lucide React (icons)

---

## 🎯 Success Criteria

### Must Have
- ✅ Timeline displays video duration
- ✅ Scene markers visible
- ✅ Click timeline to seek
- ✅ Keyboard shortcuts work
- ✅ Play/pause with Space
- ✅ Navigate scenes with [ ]
- ✅ Playhead syncs with video

### Nice to Have
- ✅ Smooth zoom/pan
- ✅ Keyframe markers
- ✅ Scene thumbnails
- ✅ Hover tooltips
- ✅ Visual feedback

---

## 📈 Estimated Timeline

| Task | Estimated | Priority |
|------|-----------|----------|
| Timeline Store | 1h | High |
| Magnetic Timeline | 2-3h | High |
| Keyboard Shortcuts | 1h | High |
| Scene Navigation | 1-2h | High |
| Playback Controls | 1h | Medium |
| Timeline-Player Sync | 1h | High |
| Zoom & Pan | 1h | Medium |
| Testing & Polish | 1h | Medium |
| **Total** | **6-8h** | |

---

## 🚀 Getting Started

1. Install dependencies
2. Create timeline store
3. Build basic timeline component
4. Add keyboard shortcuts
5. Integrate with video player
6. Test and refine

---

**Phase:** 2 - Timeline & Navigation
**Status:** Planning Complete
**Next:** Implementation
**Date:** January 6, 2026
