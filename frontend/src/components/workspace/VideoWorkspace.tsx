import { useRef, useEffect, useState } from 'react'
import { MagneticTimeline } from '@/components/timeline/MagneticTimeline'
import { PlaybackControls } from '@/components/timeline/PlaybackControls'
import { SceneNavigator } from '@/components/timeline/SceneNavigator'
import { useTimelineStore } from '@/stores/timelineStore'
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts'
import { Button } from '@/components/ui/button'
import { ChevronLeft, ChevronRight } from 'lucide-react'

interface VideoWorkspaceProps {
  videoId: number
  videoUrl: string
}

export function VideoWorkspace({ videoId, videoUrl }: VideoWorkspaceProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [showSceneNav, setShowSceneNav] = useState(true)
  const [isLoading, setIsLoading] = useState(true)

  const {
    setVideoId,
    setDuration,
    setScenes,
    setKeyframes,
    setCurrentTime,
    setIsPlaying,
    currentTime,
  } = useTimelineStore()

  // Enable keyboard shortcuts
  useKeyboardShortcuts({ enabled: true, videoRef })

  // Fetch video data
  useEffect(() => {
    setVideoId(videoId)
    setIsLoading(true)

    // Fetch video details, scenes, and keyframes
    Promise.all([
      fetch(`http://localhost:8000/api/videos/${videoId}/status`).then(r => r.json()),
      fetch(`http://localhost:8000/api/videos/${videoId}/scenes`).then(r => r.json()),
      fetch(`http://localhost:8000/api/videos/${videoId}/keyframes`).then(r => r.json()),
    ])
      .then(([status, scenesData, keyframesData]) => {
        setDuration(status.duration || 0)
        setScenes(scenesData.scenes || [])
        setKeyframes(keyframesData.keyframes || [])
        setIsLoading(false)
      })
      .catch((error) => {
        console.error('Failed to fetch video data:', error)
        setIsLoading(false)
      })
  }, [videoId, setVideoId, setDuration, setScenes, setKeyframes])

  // Sync video player with timeline store
  useEffect(() => {
    const video = videoRef.current
    if (!video) return

    const handleTimeUpdate = () => {
      setCurrentTime(video.currentTime)
    }

    const handlePlay = () => {
      setIsPlaying(true)
    }

    const handlePause = () => {
      setIsPlaying(false)
    }

    const handleLoadedMetadata = () => {
      setDuration(video.duration)
    }

    video.addEventListener('timeupdate', handleTimeUpdate)
    video.addEventListener('play', handlePlay)
    video.addEventListener('pause', handlePause)
    video.addEventListener('loadedmetadata', handleLoadedMetadata)

    return () => {
      video.removeEventListener('timeupdate', handleTimeUpdate)
      video.removeEventListener('play', handlePlay)
      video.removeEventListener('pause', handlePause)
      video.removeEventListener('loadedmetadata', handleLoadedMetadata)
    }
  }, [setCurrentTime, setIsPlaying, setDuration])

  // Sync timeline store to video player
  useEffect(() => {
    const video = videoRef.current
    if (!video) return

    // Only update if difference is significant (avoid feedback loop)
    if (Math.abs(video.currentTime - currentTime) > 0.5) {
      video.currentTime = currentTime
    }
  }, [currentTime])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-950">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4" />
          <p className="text-gray-400">Loading video workspace...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-screen flex bg-gray-950">
      {/* Main Content - Video Player & Timeline */}
      <div className={`flex-1 flex flex-col ${showSceneNav ? 'pr-80' : ''}`}>
        {/* Video Player */}
        <div className="flex-1 flex items-center justify-center bg-black p-4">
          <div className="w-full max-w-6xl">
            <video
              ref={videoRef}
              src={videoUrl}
              className="w-full rounded-lg shadow-2xl"
              controls={false}
            />
          </div>
        </div>

        {/* Playback Controls */}
        <PlaybackControls videoRef={videoRef as React.RefObject<HTMLVideoElement>} />

        {/* Magnetic Timeline */}
        <div className="p-4 bg-gray-950">
          <MagneticTimeline />
        </div>
      </div>

      {/* Scene Navigator Sidebar */}
      {showSceneNav && (
        <div className="fixed top-0 right-0 bottom-0 w-80 bg-gray-950 p-4 overflow-y-auto border-l border-gray-800">
          <SceneNavigator />
        </div>
      )}

      {/* Toggle Scene Navigator */}
      <Button
        variant="ghost"
        size="icon"
        className="fixed top-4 right-4 bg-gray-900/80 hover:bg-gray-800 backdrop-blur-sm z-10"
        onClick={() => setShowSceneNav(!showSceneNav)}
        title={showSceneNav ? 'Hide Scenes' : 'Show Scenes'}
      >
        {showSceneNav ? (
          <ChevronRight className="h-4 w-4" />
        ) : (
          <ChevronLeft className="h-4 w-4" />
        )}
      </Button>
    </div>
  )
}
