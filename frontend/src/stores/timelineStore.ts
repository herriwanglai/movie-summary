import { create } from 'zustand'

export interface Scene {
  id: number
  start_frame: number
  end_frame: number
  start_time: number
  end_time: number
  duration: number
  keyframe_count: number
}

export interface Keyframe {
  id: number
  scene_id: number
  frame_number: number
  timestamp: number
  importance_score: number
  frame_path: string | null
}

interface TimelineState {
  // Video data
  videoId: number | null
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
  setVideoId: (id: number | null) => void
  setDuration: (duration: number) => void
  setScenes: (scenes: Scene[]) => void
  setKeyframes: (keyframes: Keyframe[]) => void
  setCurrentTime: (time: number) => void
  setIsPlaying: (playing: boolean) => void
  setPlaybackRate: (rate: number) => void
  setVolume: (volume: number) => void
  setZoom: (zoom: number) => void
  setPanOffset: (offset: number) => void
  setHoveredTime: (time: number | null) => void
  setSelectedSceneId: (id: number | null) => void

  // Compound actions
  play: () => void
  pause: () => void
  togglePlay: () => void
  nextScene: () => void
  previousScene: () => void
  jumpToScene: (sceneId: number) => void
  jumpToTime: (time: number) => void
  zoomIn: () => void
  zoomOut: () => void
  resetZoom: () => void
  getCurrentScene: () => Scene | null
}

export const useTimelineStore = create<TimelineState>((set, get) => ({
  // Initial state
  videoId: null,
  duration: 0,
  scenes: [],
  keyframes: [],
  currentTime: 0,
  isPlaying: false,
  playbackRate: 1.0,
  volume: 1.0,
  zoom: 1.0,
  panOffset: 0,
  hoveredTime: null,
  selectedSceneId: null,

  // Basic setters
  setVideoId: (id) => set({ videoId: id }),
  setDuration: (duration) => set({ duration }),
  setScenes: (scenes) => set({ scenes }),
  setKeyframes: (keyframes) => set({ keyframes }),
  setCurrentTime: (time) => set({ currentTime: time }),
  setIsPlaying: (playing) => set({ isPlaying: playing }),
  setPlaybackRate: (rate) => set({ playbackRate: rate }),
  setVolume: (volume) => set({ volume: Math.max(0, Math.min(1, volume)) }),
  setZoom: (zoom) => set({ zoom: Math.max(0.5, Math.min(10, zoom)) }),
  setPanOffset: (offset) => set({ panOffset: offset }),
  setHoveredTime: (time) => set({ hoveredTime: time }),
  setSelectedSceneId: (id) => set({ selectedSceneId: id }),

  // Playback controls
  play: () => set({ isPlaying: true }),
  pause: () => set({ isPlaying: false }),
  togglePlay: () => set((state) => ({ isPlaying: !state.isPlaying })),

  // Scene navigation
  nextScene: () => {
    const { scenes, currentTime } = get()
    const currentScene = scenes.find(
      (scene) => currentTime >= scene.start_time && currentTime <= scene.end_time
    )

    if (!currentScene) {
      // Jump to first scene
      if (scenes.length > 0) {
        set({ currentTime: scenes[0].start_time, selectedSceneId: scenes[0].id })
      }
      return
    }

    const currentIndex = scenes.indexOf(currentScene)
    if (currentIndex < scenes.length - 1) {
      const nextScene = scenes[currentIndex + 1]
      set({ currentTime: nextScene.start_time, selectedSceneId: nextScene.id })
    }
  },

  previousScene: () => {
    const { scenes, currentTime } = get()
    const currentScene = scenes.find(
      (scene) => currentTime >= scene.start_time && currentTime <= scene.end_time
    )

    if (!currentScene) {
      // Jump to last scene
      if (scenes.length > 0) {
        const lastScene = scenes[scenes.length - 1]
        set({ currentTime: lastScene.start_time, selectedSceneId: lastScene.id })
      }
      return
    }

    const currentIndex = scenes.indexOf(currentScene)
    if (currentIndex > 0) {
      const prevScene = scenes[currentIndex - 1]
      set({ currentTime: prevScene.start_time, selectedSceneId: prevScene.id })
    } else {
      // Already at first scene, jump to beginning
      set({ currentTime: 0, selectedSceneId: currentScene.id })
    }
  },

  jumpToScene: (sceneId) => {
    const { scenes } = get()
    const scene = scenes.find((s) => s.id === sceneId)
    if (scene) {
      set({ currentTime: scene.start_time, selectedSceneId: sceneId })
    }
  },

  jumpToTime: (time) => {
    const { duration } = get()
    const clampedTime = Math.max(0, Math.min(duration, time))
    set({ currentTime: clampedTime })
  },

  // Zoom controls
  zoomIn: () => {
    const { zoom } = get()
    set({ zoom: Math.min(10, zoom * 1.2) })
  },

  zoomOut: () => {
    const { zoom } = get()
    set({ zoom: Math.max(0.5, zoom / 1.2) })
  },

  resetZoom: () => {
    set({ zoom: 1.0, panOffset: 0 })
  },

  // Helper
  getCurrentScene: () => {
    const { scenes, currentTime } = get()
    return scenes.find(
      (scene) => currentTime >= scene.start_time && currentTime <= scene.end_time
    ) || null
  },
}))
