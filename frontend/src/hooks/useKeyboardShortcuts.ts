import { useEffect } from 'react'
import { useTimelineStore } from '@/stores/timelineStore'

interface KeyboardShortcutsOptions {
  enabled?: boolean
  videoRef?: React.RefObject<HTMLVideoElement | null>
}

export function useKeyboardShortcuts({
  enabled = true,
  videoRef
}: KeyboardShortcutsOptions = {}) {
  const store = useTimelineStore()

  useEffect(() => {
    if (!enabled) return

    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't trigger shortcuts when typing in inputs
      const target = e.target as HTMLElement
      if (
        target.tagName === 'INPUT' ||
        target.tagName === 'TEXTAREA' ||
        target.isContentEditable
      ) {
        return
      }

      // Playback controls
      if (e.code === 'Space' || e.key === 'k' || e.key === 'K') {
        e.preventDefault()
        store.togglePlay()
        if (videoRef?.current) {
          if (store.isPlaying) {
            videoRef.current.pause()
          } else {
            videoRef.current.play()
          }
        }
      }

      // Frame navigation
      if (e.key === 'j' || e.key === 'J') {
        e.preventDefault()
        const newTime = Math.max(0, store.currentTime - 1 / 30) // 1 frame back
        store.setCurrentTime(newTime)
        if (videoRef?.current) {
          videoRef.current.currentTime = newTime
        }
      }

      if (e.key === 'l' || e.key === 'L') {
        e.preventDefault()
        const newTime = Math.min(store.duration, store.currentTime + 1 / 30) // 1 frame forward
        store.setCurrentTime(newTime)
        if (videoRef?.current) {
          videoRef.current.currentTime = newTime
        }
      }

      // Arrow keys
      if (e.key === 'ArrowLeft') {
        e.preventDefault()
        const newTime = Math.max(0, store.currentTime - 1 / 30)
        store.setCurrentTime(newTime)
        if (videoRef?.current) {
          videoRef.current.currentTime = newTime
        }
      }

      if (e.key === 'ArrowRight') {
        e.preventDefault()
        const newTime = Math.min(store.duration, store.currentTime + 1 / 30)
        store.setCurrentTime(newTime)
        if (videoRef?.current) {
          videoRef.current.currentTime = newTime
        }
      }

      // Volume controls
      if (e.key === 'ArrowUp') {
        e.preventDefault()
        const newVolume = Math.min(1, store.volume + 0.1)
        store.setVolume(newVolume)
        if (videoRef?.current) {
          videoRef.current.volume = newVolume
        }
      }

      if (e.key === 'ArrowDown') {
        e.preventDefault()
        const newVolume = Math.max(0, store.volume - 0.1)
        store.setVolume(newVolume)
        if (videoRef?.current) {
          videoRef.current.volume = newVolume
        }
      }

      // Scene navigation
      if (e.key === '[') {
        e.preventDefault()
        store.previousScene()
        if (videoRef?.current) {
          videoRef.current.currentTime = store.currentTime
        }
      }

      if (e.key === ']') {
        e.preventDefault()
        store.nextScene()
        if (videoRef?.current) {
          videoRef.current.currentTime = store.currentTime
        }
      }

      // Jump to start/end
      if (e.key === 'Home') {
        e.preventDefault()
        store.setCurrentTime(0)
        if (videoRef?.current) {
          videoRef.current.currentTime = 0
        }
      }

      if (e.key === 'End') {
        e.preventDefault()
        store.setCurrentTime(store.duration)
        if (videoRef?.current) {
          videoRef.current.currentTime = store.duration
        }
      }

      // Zoom controls
      if (e.key === '+' || e.key === '=') {
        e.preventDefault()
        store.zoomIn()
      }

      if (e.key === '-' || e.key === '_') {
        e.preventDefault()
        store.zoomOut()
      }

      if (e.key === '0' && !e.shiftKey) {
        e.preventDefault()
        store.resetZoom()
      }

      // Jump to percentage (1-9 keys)
      const num = parseInt(e.key)
      if (num >= 1 && num <= 9 && !e.shiftKey && !e.ctrlKey && !e.metaKey) {
        e.preventDefault()
        const percentage = num * 10
        const newTime = (percentage / 100) * store.duration
        store.setCurrentTime(newTime)
        if (videoRef?.current) {
          videoRef.current.currentTime = newTime
        }
      }
    }

    window.addEventListener('keydown', handleKeyDown)

    return () => {
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [enabled, videoRef, store])

  return {
    isEnabled: enabled,
  }
}
