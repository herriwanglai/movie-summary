import { useTimelineStore } from '@/stores/timelineStore'
import { Button } from '@/components/ui/button'
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Volume2,
  VolumeX,
  Rewind,
  FastForward,
} from 'lucide-react'
import { useState } from 'react'

interface PlaybackControlsProps {
  videoRef?: React.RefObject<HTMLVideoElement>
}

export function PlaybackControls({ videoRef }: PlaybackControlsProps) {
  const {
    currentTime,
    duration,
    isPlaying,
    volume,
    playbackRate,
    togglePlay,
    previousScene,
    nextScene,
    setVolume,
    setPlaybackRate,
  } = useTimelineStore()

  const [showVolumeSlider, setShowVolumeSlider] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const [previousVolume, setPreviousVolume] = useState(1)

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const handlePlayPause = () => {
    togglePlay()
    if (videoRef?.current) {
      if (isPlaying) {
        videoRef.current.pause()
      } else {
        videoRef.current.play()
      }
    }
  }

  const handlePreviousScene = () => {
    previousScene()
    if (videoRef?.current) {
      videoRef.current.currentTime = useTimelineStore.getState().currentTime
    }
  }

  const handleNextScene = () => {
    nextScene()
    if (videoRef?.current) {
      videoRef.current.currentTime = useTimelineStore.getState().currentTime
    }
  }

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVolume = parseFloat(e.target.value)
    setVolume(newVolume)
    if (videoRef?.current) {
      videoRef.current.volume = newVolume
    }
    if (newVolume > 0) {
      setIsMuted(false)
    }
  }

  const toggleMute = () => {
    if (isMuted) {
      setVolume(previousVolume)
      if (videoRef?.current) {
        videoRef.current.volume = previousVolume
      }
      setIsMuted(false)
    } else {
      setPreviousVolume(volume)
      setVolume(0)
      if (videoRef?.current) {
        videoRef.current.volume = 0
      }
      setIsMuted(true)
    }
  }

  const handlePlaybackRateChange = () => {
    const rates = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
    const currentIndex = rates.indexOf(playbackRate)
    const nextIndex = (currentIndex + 1) % rates.length
    const newRate = rates[nextIndex]
    setPlaybackRate(newRate)
    if (videoRef?.current) {
      videoRef.current.playbackRate = newRate
    }
  }

  return (
    <div className="flex items-center gap-2 px-4 py-3 bg-gray-900/50 border-t border-gray-800">
      {/* Previous Scene */}
      <Button
        variant="ghost"
        size="icon"
        onClick={handlePreviousScene}
        className="hover:bg-gray-800"
        title="Previous Scene ([)"
      >
        <SkipBack className="h-4 w-4" />
      </Button>

      {/* Rewind */}
      <Button
        variant="ghost"
        size="icon"
        onClick={() => {
          const newTime = Math.max(0, currentTime - 10)
          useTimelineStore.getState().setCurrentTime(newTime)
          if (videoRef?.current) {
            videoRef.current.currentTime = newTime
          }
        }}
        className="hover:bg-gray-800"
        title="Rewind 10s (J)"
      >
        <Rewind className="h-4 w-4" />
      </Button>

      {/* Play/Pause */}
      <Button
        variant="ghost"
        size="icon"
        onClick={handlePlayPause}
        className="hover:bg-gray-800"
        title="Play/Pause (Space/K)"
      >
        {isPlaying ? (
          <Pause className="h-5 w-5" />
        ) : (
          <Play className="h-5 w-5 ml-0.5" />
        )}
      </Button>

      {/* Fast Forward */}
      <Button
        variant="ghost"
        size="icon"
        onClick={() => {
          const newTime = Math.min(duration, currentTime + 10)
          useTimelineStore.getState().setCurrentTime(newTime)
          if (videoRef?.current) {
            videoRef.current.currentTime = newTime
          }
        }}
        className="hover:bg-gray-800"
        title="Forward 10s (L)"
      >
        <FastForward className="h-4 w-4" />
      </Button>

      {/* Next Scene */}
      <Button
        variant="ghost"
        size="icon"
        onClick={handleNextScene}
        className="hover:bg-gray-800"
        title="Next Scene (])"
      >
        <SkipForward className="h-4 w-4" />
      </Button>

      {/* Time Display */}
      <div className="flex items-center gap-2 text-sm tabular-nums px-3">
        <span className="text-white font-medium">{formatTime(currentTime)}</span>
        <span className="text-gray-500">/</span>
        <span className="text-gray-400">{formatTime(duration)}</span>
      </div>

      {/* Spacer */}
      <div className="flex-1" />

      {/* Playback Rate */}
      <Button
        variant="ghost"
        size="sm"
        onClick={handlePlaybackRateChange}
        className="hover:bg-gray-800 text-xs font-medium min-w-[3rem]"
        title="Change playback speed"
      >
        {playbackRate}x
      </Button>

      {/* Volume Control */}
      <div
        className="relative flex items-center gap-2"
        onMouseEnter={() => setShowVolumeSlider(true)}
        onMouseLeave={() => setShowVolumeSlider(false)}
      >
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleMute}
          className="hover:bg-gray-800"
          title={isMuted ? "Unmute" : "Mute"}
        >
          {isMuted || volume === 0 ? (
            <VolumeX className="h-4 w-4" />
          ) : (
            <Volume2 className="h-4 w-4" />
          )}
        </Button>

        {/* Volume Slider */}
        {showVolumeSlider && (
          <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 p-2 bg-gray-900 border border-gray-700 rounded shadow-lg">
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={volume}
              onChange={handleVolumeChange}
              className="w-24 h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer
                [&::-webkit-slider-thumb]:appearance-none
                [&::-webkit-slider-thumb]:w-3
                [&::-webkit-slider-thumb]:h-3
                [&::-webkit-slider-thumb]:rounded-full
                [&::-webkit-slider-thumb]:bg-white
                [&::-webkit-slider-thumb]:cursor-pointer"
            />
          </div>
        )}
      </div>

      {/* Keyboard Hints */}
      <div className="text-[10px] text-gray-600 px-2 border-l border-gray-800 hidden lg:block">
        <span className="font-mono">Space</span> Play/Pause •{' '}
        <span className="font-mono">J/L</span> Frame •{' '}
        <span className="font-mono">[ ]</span> Scene
      </div>
    </div>
  )
}
