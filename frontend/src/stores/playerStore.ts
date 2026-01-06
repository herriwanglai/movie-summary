import { create } from 'zustand'

interface PlayerStore {
  // Playback state
  isPlaying: boolean
  currentTime: number
  duration: number
  volume: number
  isMuted: boolean
  playbackRate: number
  isFullscreen: boolean

  // UI state
  showControls: boolean
  showTimeline: boolean
  showSubtitles: boolean

  // Screenshot state
  screenshots: Screenshot[]

  // Actions
  setPlaying: (isPlaying: boolean) => void
  setCurrentTime: (time: number) => void
  setDuration: (duration: number) => void
  setVolume: (volume: number) => void
  setMuted: (isMuted: boolean) => void
  setPlaybackRate: (rate: number) => void
  setFullscreen: (isFullscreen: boolean) => void
  setShowControls: (show: boolean) => void
  setShowTimeline: (show: boolean) => void
  setShowSubtitles: (show: boolean) => void
  addScreenshot: (screenshot: Screenshot) => void
  removeScreenshot: (id: string) => void
  clearScreenshots: () => void

  // Player controls
  play: () => void
  pause: () => void
  togglePlay: () => void
  seek: (time: number) => void
  skipForward: (seconds: number) => void
  skipBackward: (seconds: number) => void
  toggleMute: () => void
  toggleFullscreen: () => void
}

export interface Screenshot {
  id: string
  dataUrl: string
  timestamp: number
  createdAt: string
}

export const usePlayerStore = create<PlayerStore>((set) => ({
  // Initial state
  isPlaying: false,
  currentTime: 0,
  duration: 0,
  volume: 1,
  isMuted: false,
  playbackRate: 1,
  isFullscreen: false,
  showControls: true,
  showTimeline: true,
  showSubtitles: false,
  screenshots: [],

  // Setters
  setPlaying: (isPlaying) => set({ isPlaying }),
  setCurrentTime: (currentTime) => set({ currentTime }),
  setDuration: (duration) => set({ duration }),
  setVolume: (volume) => set({ volume }),
  setMuted: (isMuted) => set({ isMuted }),
  setPlaybackRate: (playbackRate) => set({ playbackRate }),
  setFullscreen: (isFullscreen) => set({ isFullscreen }),
  setShowControls: (showControls) => set({ showControls }),
  setShowTimeline: (showTimeline) => set({ showTimeline }),
  setShowSubtitles: (showSubtitles) => set({ showSubtitles }),

  // Screenshot management
  addScreenshot: (screenshot) =>
    set((state) => ({
      screenshots: [...state.screenshots, screenshot],
    })),
  removeScreenshot: (id) =>
    set((state) => ({
      screenshots: state.screenshots.filter((s) => s.id !== id),
    })),
  clearScreenshots: () => set({ screenshots: [] }),

  // Player controls
  play: () => set({ isPlaying: true }),
  pause: () => set({ isPlaying: false }),
  togglePlay: () => set((state) => ({ isPlaying: !state.isPlaying })),
  seek: (time) => set({ currentTime: time }),
  skipForward: (seconds) =>
    set((state) => ({ currentTime: Math.min(state.currentTime + seconds, state.duration) })),
  skipBackward: (seconds) =>
    set((state) => ({ currentTime: Math.max(state.currentTime - seconds, 0) })),
  toggleMute: () => set((state) => ({ isMuted: !state.isMuted })),
  toggleFullscreen: () => set((state) => ({ isFullscreen: !state.isFullscreen })),
}))
