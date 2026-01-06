# Enhanced Features: Magnetic Timeline & Jump Navigation

## 🎬 Apple Final Cut Pro Inspired Magnetic Timeline

### Overview
The timeline will use a **Magnetic Timeline** design similar to Final Cut Pro, where:
- Clips and keyframes snap and attach to each other
- Dragging items automatically adjusts surrounding elements
- Multi-track layout with scene blocks, screenshots, clips, and annotations
- Easy navigation between keyframes with snap points

---

## 🧲 Magnetic Timeline Features

### 1. Multi-Track Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Importance Graph  ▁▃▅▇█▇▅▃▁▃▅▇█                            │
├─────────────────────────────────────────────────────────────┤
│ Scene Track      [Scene 1][Scene 2]  [Scene 3][Scene 4]    │
├─────────────────────────────────────────────────────────────┤
│ Screenshots       📸    📸  📸         📸                    │
├─────────────────────────────────────────────────────────────┤
│ Clips            [═══════]      [════════]                  │
├─────────────────────────────────────────────────────────────┤
│ Annotations       💬         💬    💬                        │
├─────────────────────────────────────────────────────────────┤
│ Playhead         ════════════════●══════════════════        │
│                              01:23:45                        │
└─────────────────────────────────────────────────────────────┘
```

### 2. Magnetic Snapping

**Keyframe Navigation:**
- Press `K` - Snap to next keyframe (screenshot/clip/scene change)
- Press `J` - Snap to previous keyframe
- Click on any track item - Playhead jumps to that position
- Drag playhead - Snaps to nearest keyframe when close

**Visual Feedback:**
- Snap indicators appear when approaching keyframes
- Highlight active track item
- Show timestamp tooltip on hover

### 3. Track Features

#### Scene Track
```typescript
interface SceneBlock {
  sceneNumber: number;
  startTime: number;
  endTime: number;
  importanceScore: number;
  color: string; // Intensity-based color
  thumbnail: string;
  isActive: boolean; // Currently playing
}

// Visual representation
<SceneBlock
  onClick={() => jumpToTime(scene.startTime)}
  color={getImportanceColor(scene.importanceScore)}
  height={40}
  showThumbnail={zoomLevel > 2}
/>
```

#### Screenshot Track
```typescript
interface ScreenshotMarker {
  id: string;
  timestamp: number;
  thumbnail: string;
  hasAnnotation: boolean;
  linkedToNode: boolean; // If added to node editor
}

// Magnetic snap points
const snapPoints = screenshots.map(s => s.timestamp);

// Jump navigation
<ScreenshotMarker
  onClick={() => {
    jumpToTime(screenshot.timestamp);
    highlightInCollection(screenshot.id);
    highlightInNodeEditor(screenshot.id);
  }}
  onDoubleClick={() => openScreenshotPreview(screenshot.id)}
/>
```

#### Clip Track
```typescript
interface ClipRange {
  id: string;
  startTime: number;
  endTime: number;
  thumbnail: string;
  isPlaying: boolean;
}

// Clips show as ranges with handles
<ClipRange
  onClick={() => jumpToTime(clip.startTime)}
  onDragStart={() => enableClipResize(clip.id)}
  onDragEnd={() => updateClipBoundaries()}
  handles={['start', 'end']} // Resizable
/>
```

---

## 🔗 Jump Navigation System

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                Global Navigation State                   │
│  - currentTime: number                                   │
│  - jumpToTime(timestamp: number)                         │
│  - highlightItem(id: string, type: string)              │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
┌─────────────┐ ┌──────────┐ ┌─────────────┐
│  Collection │ │   Node   │ │   Timeline  │
│   Manager   │ │  Editor  │ │             │
└─────────────┘ └──────────┘ └─────────────┘
```

### 1. Collection Manager → Timeline Jump

**Screenshot Gallery:**
```typescript
<ScreenshotCard
  screenshot={screenshot}
  onClick={() => {
    // Jump to timeline
    videoPlayer.seekTo(screenshot.timestamp);

    // Highlight in timeline
    timeline.highlightMarker(screenshot.id);

    // Auto-scroll timeline to view
    timeline.scrollToTime(screenshot.timestamp);

    // Flash highlight
    timeline.flashMarker(screenshot.id, 1000);
  }}
>
  <img src={screenshot.thumbnail} />
  <div className="overlay">
    <button className="jump-btn" title="Jump to Timeline">
      ⏱️ {formatTime(screenshot.timestamp)}
    </button>
    <button className="play-btn" title="Play from here">
      ▶️
    </button>
  </div>
</ScreenshotCard>
```

**Clip Library:**
```typescript
<ClipCard
  clip={clip}
  onClick={() => {
    // Jump to clip start
    videoPlayer.seekTo(clip.startTime);

    // Highlight clip range in timeline
    timeline.highlightClipRange(clip.id);

    // Auto-scroll
    timeline.scrollToTime(clip.startTime);
  }}
  onPlayClick={() => {
    // Play just this clip
    videoPlayer.playRange(clip.startTime, clip.endTime);

    // Highlight during playback
    timeline.trackPlayback(clip.startTime, clip.endTime);
  }}
>
  <video src={clip.thumbnailUrl} />
  <div className="info">
    <span className="duration">{formatDuration(clip.duration)}</span>
    <button className="jump-btn">
      🎯 Jump to Timeline
    </button>
    <button className="play-btn">
      ▶️ Play Clip
    </button>
  </div>
</ClipCard>
```

### 2. Node Editor → Timeline Jump

**Screenshot Node:**
```typescript
<ScreenshotNode
  data={screenshot}
  onDoubleClick={() => {
    // Jump to video player
    videoPlayer.seekTo(screenshot.timestamp);

    // Highlight in timeline
    timeline.highlightAndScroll(screenshot.timestamp);

    // Highlight in collection
    collection.scrollToItem(screenshot.id);

    // Optional: Switch to video player tab
    switchToTab('video-player');
  }}
>
  <div className="node-content">
    <img src={screenshot.thumbnail} />
    <div className="node-toolbar">
      <button
        onClick={(e) => {
          e.stopPropagation();
          jumpToTimeline(screenshot.timestamp);
        }}
        className="jump-btn-small"
        title="Jump to Timeline"
      >
        🎬
      </button>
      <span className="timestamp">
        {formatTime(screenshot.timestamp)}
      </span>
    </div>
  </div>
</ScreenshotNode>
```

**Clip Node:**
```typescript
<ClipNode
  data={clip}
  onDoubleClick={() => {
    videoPlayer.playRange(clip.startTime, clip.endTime);
    timeline.highlightClipRange(clip.id);
  }}
>
  <div className="node-content">
    <video src={clip.thumbnailUrl} loop muted />
    <div className="node-toolbar">
      <button
        onClick={(e) => {
          e.stopPropagation();
          jumpToTimeline(clip.startTime);
        }}
        className="jump-btn-small"
      >
        🎬 Jump
      </button>
      <button
        onClick={(e) => {
          e.stopPropagation();
          playClipRange(clip);
        }}
        className="play-btn-small"
      >
        ▶️ Play
      </button>
      <span className="duration">
        {formatDuration(clip.duration)}
      </span>
    </div>
  </div>
</ClipNode>
```

**Scene Node:**
```typescript
<SceneNode
  data={scene}
  onClick={() => {
    jumpToTimeline(scene.startTime);
  }}
>
  <div className="scene-header">
    <span>Scene {scene.sceneNumber}</span>
    <button
      className="jump-btn-icon"
      onClick={(e) => {
        e.stopPropagation();
        jumpToTimeline(scene.startTime);
      }}
    >
      ⏱️
    </button>
  </div>
  <img src={scene.thumbnail} />
  <div className="scene-footer">
    <span>{formatTimeRange(scene.startTime, scene.endTime)}</span>
    <ImportanceIndicator score={scene.importanceScore} />
  </div>
</SceneNode>
```

---

## 🎮 Keyboard Shortcuts (Final Cut Pro Style)

```typescript
const keyboardShortcuts = {
  // Playback
  'Space': 'togglePlayPause',
  'J': 'previousKeyframe',    // Magnetic snap
  'K': 'nextKeyframe',         // Magnetic snap
  'L': 'playForward',
  'I': 'markClipStart',
  'O': 'markClipEnd',

  // Navigation
  'ArrowLeft': 'frameBackward',
  'ArrowRight': 'frameForward',
  'Shift+ArrowLeft': 'previousScene',
  'Shift+ArrowRight': 'nextScene',

  // Actions
  'Cmd+S': 'captureScreenshot',
  'Cmd+Shift+S': 'saveAnnotations',
  'Cmd+E': 'createClip',

  // Timeline
  '+': 'zoomIn',
  '-': 'zoomOut',
  'Z': 'fitToWindow',

  // Selection
  'A': 'selectAll',
  'Cmd+D': 'deselectAll',
};
```

---

## 💡 Implementation Details

### 1. Global Navigation Hook

```typescript
// hooks/useNavigation.ts
import { create } from 'zustand';

interface NavigationState {
  currentTime: number;
  isPlaying: boolean;
  selectedItems: Set<string>;

  // Actions
  jumpToTime: (timestamp: number) => void;
  highlightItem: (id: string, type: 'screenshot' | 'clip' | 'scene') => void;
  playRange: (start: number, end: number) => void;

  // Sync across components
  syncVideoPlayer: () => void;
  syncTimeline: () => void;
  syncCollection: () => void;
  syncNodeEditor: () => void;
}

export const useNavigation = create<NavigationState>((set, get) => ({
  currentTime: 0,
  isPlaying: false,
  selectedItems: new Set(),

  jumpToTime: (timestamp) => {
    set({ currentTime: timestamp });

    // Broadcast to all components
    window.dispatchEvent(new CustomEvent('timeline:jump', {
      detail: { timestamp }
    }));
  },

  highlightItem: (id, type) => {
    set((state) => ({
      selectedItems: new Set([...state.selectedItems, id])
    }));

    // Flash highlight
    setTimeout(() => {
      set((state) => {
        const items = new Set(state.selectedItems);
        items.delete(id);
        return { selectedItems: items };
      });
    }, 2000);
  },

  playRange: (start, end) => {
    get().jumpToTime(start);
    set({ isPlaying: true });

    // Stop at end
    const stopTimer = setTimeout(() => {
      set({ isPlaying: false });
    }, (end - start) * 1000);
  }
}));
```

### 2. Magnetic Timeline Component

```typescript
// components/MagneticTimeline/MagneticTimeline.tsx
interface MagneticTimelineProps {
  duration: number;
  scenes: Scene[];
  screenshots: Screenshot[];
  clips: Clip[];
  annotations: Annotation[];
  currentTime: number;
  onTimeChange: (time: number) => void;
}

export const MagneticTimeline: React.FC<MagneticTimelineProps> = ({
  duration,
  scenes,
  screenshots,
  clips,
  currentTime,
  onTimeChange
}) => {
  const [zoomLevel, setZoomLevel] = useState(1); // pixels per second
  const [snapEnabled, setSnapEnabled] = useState(true);
  const timelineRef = useRef<HTMLDivElement>(null);

  // Calculate snap points
  const snapPoints = useMemo(() => {
    const points = [
      ...scenes.flatMap(s => [s.startTime, s.endTime]),
      ...screenshots.map(s => s.timestamp),
      ...clips.flatMap(c => [c.startTime, c.endTime])
    ];
    return [...new Set(points)].sort((a, b) => a - b);
  }, [scenes, screenshots, clips]);

  // Find nearest snap point
  const findNearestSnap = (time: number, threshold = 0.5) => {
    if (!snapEnabled) return time;

    const nearest = snapPoints.reduce((prev, curr) => {
      return Math.abs(curr - time) < Math.abs(prev - time) ? curr : prev;
    });

    return Math.abs(nearest - time) < threshold ? nearest : time;
  };

  // Handle click to jump
  const handleTimelineClick = (e: React.MouseEvent) => {
    const rect = timelineRef.current?.getBoundingClientRect();
    if (!rect) return;

    const clickX = e.clientX - rect.left;
    const time = (clickX / rect.width) * duration;
    const snappedTime = findNearestSnap(time);

    onTimeChange(snappedTime);
  };

  // Keyboard navigation
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === 'j') {
        // Previous keyframe
        const prev = snapPoints.reverse().find(t => t < currentTime);
        if (prev !== undefined) onTimeChange(prev);
      } else if (e.key === 'k') {
        // Next keyframe
        const next = snapPoints.find(t => t > currentTime);
        if (next !== undefined) onTimeChange(next);
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [currentTime, snapPoints]);

  return (
    <div className="magnetic-timeline" ref={timelineRef}>
      {/* Importance Graph Track */}
      <ImportanceGraphTrack scenes={scenes} />

      {/* Scene Track */}
      <SceneTrack
        scenes={scenes}
        currentTime={currentTime}
        onSceneClick={(scene) => onTimeChange(scene.startTime)}
      />

      {/* Screenshot Track */}
      <ScreenshotTrack
        screenshots={screenshots}
        currentTime={currentTime}
        onScreenshotClick={(screenshot) => {
          onTimeChange(screenshot.timestamp);
          // Also highlight in collection and node editor
          window.dispatchEvent(new CustomEvent('highlight:screenshot', {
            detail: { id: screenshot.id }
          }));
        }}
      />

      {/* Clip Track */}
      <ClipTrack
        clips={clips}
        currentTime={currentTime}
        onClipClick={(clip) => onTimeChange(clip.startTime)}
      />

      {/* Playhead */}
      <Playhead
        time={currentTime}
        snapPoints={snapPoints}
        snapEnabled={snapEnabled}
        onDrag={(time) => onTimeChange(findNearestSnap(time))}
      />

      {/* Time Ruler */}
      <TimeRuler duration={duration} zoomLevel={zoomLevel} />
    </div>
  );
};
```

### 3. Jump Button Component

```typescript
// components/JumpButton/JumpButton.tsx
interface JumpButtonProps {
  timestamp: number;
  label?: string;
  variant?: 'icon' | 'text' | 'both';
  size?: 'small' | 'medium' | 'large';
  showTime?: boolean;
}

export const JumpButton: React.FC<JumpButtonProps> = ({
  timestamp,
  label = 'Jump to Timeline',
  variant = 'both',
  size = 'medium',
  showTime = true
}) => {
  const { jumpToTime, highlightItem } = useNavigation();

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation(); // Don't trigger parent click

    // Jump to time
    jumpToTime(timestamp);

    // Visual feedback
    toast.success(`Jumped to ${formatTime(timestamp)}`);
  };

  return (
    <button
      onClick={handleClick}
      className={`jump-button jump-button-${variant} jump-button-${size}`}
      title={label}
    >
      {(variant === 'icon' || variant === 'both') && (
        <span className="icon">🎬</span>
      )}
      {(variant === 'text' || variant === 'both') && (
        <span className="label">{label}</span>
      )}
      {showTime && (
        <span className="timestamp">{formatTime(timestamp)}</span>
      )}
    </button>
  );
};
```

---

## 🎨 Visual Design Updates

### Collection Manager with Jump Buttons

```tsx
<ScreenshotCard>
  <img src={screenshot.thumbnail} />

  {/* Hover overlay */}
  <div className="hover-overlay">
    <div className="action-buttons">
      <JumpButton
        timestamp={screenshot.timestamp}
        variant="icon"
        size="large"
      />
      <button className="preview-btn">👁️ Preview</button>
      <button className="delete-btn">🗑️ Delete</button>
    </div>
  </div>

  {/* Info bar */}
  <div className="info-bar">
    <span className="time">{formatTime(screenshot.timestamp)}</span>
    <span className="scene">Scene {screenshot.sceneNumber}</span>
    {screenshot.linkedToNode && <span className="badge">📊 In Graph</span>}
  </div>
</ScreenshotCard>
```

### Node Editor with Jump Controls

```tsx
<ScreenshotNode>
  <div className="node-header">
    <span className="node-title">Screenshot</span>
    <div className="node-controls">
      <JumpButton
        timestamp={data.timestamp}
        variant="icon"
        size="small"
      />
      <button className="play-btn-icon">▶️</button>
    </div>
  </div>

  <img src={data.thumbnail} className="node-image" />

  <div className="node-footer">
    <span className="timestamp">{formatTime(data.timestamp)}</span>
    <ImportanceBadge score={data.importanceScore} />
  </div>
</ScreenshotNode>
```

---

## 📊 Updated Component Communication

```
User Action: Click "Jump" in Collection Manager
     ↓
useNavigation.jumpToTime(timestamp)
     ↓
Event: 'timeline:jump' dispatched
     ↓
┌────────────────┬────────────────┬────────────────┐
│  Video Player  │   Timeline     │  Node Editor   │
│  - Seeks to    │  - Scrolls to  │  - Highlights  │
│    timestamp   │    position    │    node        │
│  - Pauses      │  - Flashes     │  - Scrolls     │
│               │    marker      │    into view   │
└────────────────┴────────────────┴────────────────┘
```

---

## ✅ Updated Task List

| # | Task | Enhancement |
|---|------|-------------|
| 1 | Design architecture | ✅ Updated with navigation system |
| 2 | React project setup | - |
| 3 | **Magnetic Timeline** | 🆕 Multi-track with snap points |
| 4 | Node editor integration | 🆕 Jump buttons on all nodes |
| 5 | **Collection manager** | 🆕 Jump buttons on cards |
| 6 | FastAPI backend | - |
| 7 | Annotation persistence | - |
| 8 | **Navigation system** | 🆕 Global navigation state |
| 9 | Export functionality | - |
| 10 | Integration & polish | - |

---

## 🚀 Summary of Enhancements

### 1. Magnetic Timeline (Final Cut Pro Style)
✅ Multi-track layout (scenes, screenshots, clips, annotations)
✅ Snap-to-keyframe navigation (J/K keys)
✅ Visual importance graph
✅ Click any track item to jump
✅ Draggable playhead with snap

### 2. Jump Navigation from Collection Manager
✅ Jump button on every screenshot card
✅ Jump button on every clip card
✅ Auto-scroll timeline to position
✅ Highlight marker with flash effect
✅ Optional: Auto-play from position

### 3. Jump Navigation from Node Editor
✅ Jump button on screenshot nodes
✅ Jump button on clip nodes
✅ Jump button on scene nodes
✅ Double-click to jump and play
✅ Syncs with timeline and collection

### 4. Global Navigation System
✅ Shared state across all components
✅ Event-based communication
✅ Consistent UX across interface
✅ Keyboard shortcuts (J/K navigation)

**Ready to implement with these enhancements!** 🎬✨
