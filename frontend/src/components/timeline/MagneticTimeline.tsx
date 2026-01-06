import { useRef, useEffect, useState } from 'react'
import { useTimelineStore } from '@/stores/timelineStore'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

interface MagneticTimelineProps {
  className?: string
}

export function MagneticTimeline({ className }: MagneticTimelineProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [isDragging, setIsDragging] = useState(false)

  const {
    duration,
    currentTime,
    scenes,
    keyframes,
    zoom,
    hoveredTime,
    setHoveredTime,
    jumpToTime,
    zoomIn,
    zoomOut,
  } = useTimelineStore()

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    const ms = Math.floor((seconds % 1) * 100)
    return `${mins}:${secs.toString().padStart(2, '0')}.${ms.toString().padStart(2, '0')}`
  }

  const handleClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!containerRef.current || duration === 0) return

    const rect = containerRef.current.getBoundingClientRect()
    const x = e.clientX - rect.left
    const percentage = x / rect.width
    const time = percentage * duration

    jumpToTime(time)
  }

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!containerRef.current || duration === 0) return

    const rect = containerRef.current.getBoundingClientRect()
    const x = e.clientX - rect.left
    const percentage = x / rect.width
    const time = percentage * duration

    setHoveredTime(time)

    if (isDragging) {
      jumpToTime(time)
    }
  }

  const handleMouseLeave = () => {
    setHoveredTime(null)
  }

  const handleMouseDown = () => {
    setIsDragging(true)
  }

  useEffect(() => {
    const handleMouseUp = () => {
      setIsDragging(false)
    }

    window.addEventListener('mouseup', handleMouseUp)
    return () => window.removeEventListener('mouseup', handleMouseUp)
  }, [])

  // Handle wheel for zoom
  const handleWheel = (e: React.WheelEvent<HTMLDivElement>) => {
    if (e.ctrlKey || e.metaKey) {
      e.preventDefault()
      if (e.deltaY < 0) {
        zoomIn()
      } else {
        zoomOut()
      }
    }
  }

  if (duration === 0) {
    return (
      <div className={cn('h-24 bg-gray-900/50 rounded flex items-center justify-center', className)}>
        <p className="text-sm text-muted-foreground">No video loaded</p>
      </div>
    )
  }

  const playheadPosition = (currentTime / duration) * 100

  return (
    <div className={cn('relative bg-gray-950 border border-gray-800 rounded-lg overflow-hidden', className)}>
      {/* Time ruler */}
      <div className="h-6 bg-gray-900/50 border-b border-gray-800 px-2 flex items-center text-[10px] text-gray-400">
        <span className="mr-4">{formatTime(0)}</span>
        {Array.from({ length: 9 }).map((_, i) => {
          const time = ((i + 1) / 10) * duration
          return (
            <span key={i} className="flex-1 text-center">
              {formatTime(time)}
            </span>
          )
        })}
        <span className="ml-4">{formatTime(duration)}</span>
      </div>

      {/* Timeline track */}
      <div
        ref={containerRef}
        className="relative h-16 bg-gray-900/30 cursor-pointer select-none"
        onClick={handleClick}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        onMouseDown={handleMouseDown}
        onWheel={handleWheel}
      >
        {/* Scene markers */}
        {scenes.map((scene, index) => {
          const startPercent = (scene.start_time / duration) * 100
          const widthPercent = ((scene.end_time - scene.start_time) / duration) * 100

          return (
            <div
              key={scene.id}
              className="absolute top-0 bottom-0 border-l border-r border-blue-500/30 bg-blue-500/10 hover:bg-blue-500/20 transition-colors group"
              style={{
                left: `${startPercent}%`,
                width: `${widthPercent}%`,
              }}
            >
              {/* Scene label */}
              <div className="absolute top-1 left-1 text-[9px] text-blue-400 font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                Scene {index + 1}
              </div>

              {/* Keyframe markers */}
              {keyframes
                .filter((kf) => kf.scene_id === scene.id)
                .map((keyframe) => {
                  const kfPercent = ((keyframe.timestamp - scene.start_time) / (scene.end_time - scene.start_time)) * 100
                  return (
                    <div
                      key={keyframe.id}
                      className="absolute bottom-2 w-1 h-3 bg-green-500 rounded-full"
                      style={{ left: `${kfPercent}%` }}
                      title={`Keyframe at ${formatTime(keyframe.timestamp)}`}
                    />
                  )
                })}
            </div>
          )
        })}

        {/* Hovered time indicator */}
        {hoveredTime !== null && (
          <div
            className="absolute top-0 bottom-0 w-px bg-white/30 pointer-events-none"
            style={{ left: `${(hoveredTime / duration) * 100}%` }}
          >
            <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-black/90 text-white text-[10px] px-2 py-0.5 rounded whitespace-nowrap">
              {formatTime(hoveredTime)}
            </div>
          </div>
        )}

        {/* Playhead */}
        <motion.div
          className="absolute top-0 bottom-0 w-0.5 bg-white shadow-lg pointer-events-none z-10"
          style={{ left: `${playheadPosition}%` }}
          initial={false}
          animate={{ left: `${playheadPosition}%` }}
          transition={{ type: 'tween', duration: 0.1 }}
        >
          {/* Playhead handle */}
          <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 w-3 h-3 bg-white rounded-full shadow-lg" />
          {/* Current time label */}
          <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 bg-white text-black text-[10px] font-medium px-2 py-0.5 rounded whitespace-nowrap">
            {formatTime(currentTime)}
          </div>
        </motion.div>
      </div>

      {/* Zoom indicator */}
      {zoom !== 1 && (
        <div className="absolute top-2 right-2 bg-black/70 text-white text-[10px] px-2 py-1 rounded">
          {(zoom * 100).toFixed(0)}%
        </div>
      )}
    </div>
  )
}
