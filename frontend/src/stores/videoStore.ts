import { create } from 'zustand'

export interface Video {
  id: string
  title: string
  filename: string
  duration: number
  fileSize: number
  mimeType: string
  uploadedAt: string
  processingStatus: 'pending' | 'processing' | 'complete' | 'error'
  streamUrl?: string
  thumbnailUrl?: string
}

export interface Scene {
  id: string
  videoId: string
  startTime: number
  endTime: number
  description: string
  thumbnailUrl?: string
}

export interface Keyframe {
  id: string
  videoId: string
  timestamp: number
  description: string
  imageUrl: string
}

interface VideoStore {
  currentVideo: Video | null
  videos: Video[]
  scenes: Scene[]
  keyframes: Keyframe[]
  isLoading: boolean
  error: string | null

  // Actions
  setCurrentVideo: (video: Video) => void
  setVideos: (videos: Video[]) => void
  addVideo: (video: Video) => void
  updateVideo: (id: string, updates: Partial<Video>) => void
  setScenes: (scenes: Scene[]) => void
  setKeyframes: (keyframes: Keyframe[]) => void
  setLoading: (isLoading: boolean) => void
  setError: (error: string | null) => void

  // Async actions
  fetchVideo: (videoId: string) => Promise<void>
  fetchVideos: () => Promise<void>
  fetchScenes: (videoId: string) => Promise<void>
  fetchKeyframes: (videoId: string) => Promise<void>
}

export const useVideoStore = create<VideoStore>((set) => ({
  currentVideo: null,
  videos: [],
  scenes: [],
  keyframes: [],
  isLoading: false,
  error: null,

  setCurrentVideo: (video) => set({ currentVideo: video }),
  setVideos: (videos) => set({ videos }),
  addVideo: (video) => set((state) => ({ videos: [...state.videos, video] })),
  updateVideo: (id, updates) =>
    set((state) => ({
      videos: state.videos.map((v) => (v.id === id ? { ...v, ...updates } : v)),
      currentVideo:
        state.currentVideo?.id === id
          ? { ...state.currentVideo, ...updates }
          : state.currentVideo,
    })),
  setScenes: (scenes) => set({ scenes }),
  setKeyframes: (keyframes) => set({ keyframes }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),

  fetchVideo: async (videoId) => {
    set({ isLoading: true, error: null })
    try {
      const response = await fetch(`http://localhost:8000/api/videos/${videoId}`)
      if (!response.ok) throw new Error('Failed to fetch video')
      const video = await response.json()
      set({ currentVideo: video, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Unknown error',
        isLoading: false,
      })
    }
  },

  fetchVideos: async () => {
    set({ isLoading: true, error: null })
    try {
      const response = await fetch('http://localhost:8000/api/videos')
      if (!response.ok) throw new Error('Failed to fetch videos')
      const videos = await response.json()
      set({ videos, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Unknown error',
        isLoading: false,
      })
    }
  },

  fetchScenes: async (videoId) => {
    set({ isLoading: true, error: null })
    try {
      const response = await fetch(`http://localhost:8000/api/videos/${videoId}/scenes`)
      if (!response.ok) throw new Error('Failed to fetch scenes')
      const scenes = await response.json()
      set({ scenes, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Unknown error',
        isLoading: false,
      })
    }
  },

  fetchKeyframes: async (videoId) => {
    set({ isLoading: true, error: null })
    try {
      const response = await fetch(`http://localhost:8000/api/videos/${videoId}/keyframes`)
      if (!response.ok) throw new Error('Failed to fetch keyframes')
      const keyframes = await response.json()
      set({ keyframes, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Unknown error',
        isLoading: false,
      })
    }
  },
}))
