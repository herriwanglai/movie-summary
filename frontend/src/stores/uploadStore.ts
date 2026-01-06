import { create } from 'zustand'

export interface UploadState {
  uploadId: string | null
  fileName: string | null
  fileSize: number
  progress: number
  status: 'idle' | 'uploading' | 'processing' | 'complete' | 'error'
  error: string | null
  videoId: string | null
}

interface UploadStore extends UploadState {
  setUploadId: (uploadId: string) => void
  setFileName: (fileName: string) => void
  setFileSize: (fileSize: number) => void
  setProgress: (progress: number) => void
  setStatus: (status: UploadState['status']) => void
  setError: (error: string | null) => void
  setVideoId: (videoId: string) => void
  resetUpload: () => void
}

const initialState: UploadState = {
  uploadId: null,
  fileName: null,
  fileSize: 0,
  progress: 0,
  status: 'idle',
  error: null,
  videoId: null,
}

export const useUploadStore = create<UploadStore>((set) => ({
  ...initialState,

  setUploadId: (uploadId) => set({ uploadId }),
  setFileName: (fileName) => set({ fileName }),
  setFileSize: (fileSize) => set({ fileSize }),
  setProgress: (progress) => set({ progress }),
  setStatus: (status) => set({ status }),
  setError: (error) => set({ error }),
  setVideoId: (videoId) => set({ videoId }),
  resetUpload: () => set(initialState),
}))
