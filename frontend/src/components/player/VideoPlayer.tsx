import { useRef, useCallback } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { useToast } from '@/hooks/use-toast'
import { Camera } from 'lucide-react'

interface VideoPlayerProps {
  src: string
  title?: string
  poster?: string
  onTimeUpdate?: (time: number) => void
  onScreenshot?: (dataUrl: string, timestamp: number) => void
}

export function VideoPlayer({
  src,
  title = 'Video',
  poster,
  onTimeUpdate,
  onScreenshot
}: VideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const { toast } = useToast()

  const handleScreenshot = useCallback(async () => {
    if (!videoRef.current) {
      toast({
        variant: 'destructive',
        title: 'Screenshot failed',
        description: 'Video not ready',
      })
      return
    }

    try {
      const canvas = document.createElement('canvas')
      const video = videoRef.current

      canvas.width = video.videoWidth
      canvas.height = video.videoHeight

      const ctx = canvas.getContext('2d')
      if (!ctx) {
        throw new Error('Failed to get canvas context')
      }

      ctx.drawImage(video, 0, 0)
      const dataUrl = canvas.toDataURL('image/png')
      const currentTime = video.currentTime

      onScreenshot?.(dataUrl, currentTime)

      toast({
        title: 'Screenshot captured',
        description: `Captured at ${formatTimestamp(currentTime)}`,
      })
    } catch (error) {
      console.error('Screenshot error:', error)
      toast({
        variant: 'destructive',
        title: 'Screenshot failed',
        description: error instanceof Error ? error.message : 'Unknown error',
      })
    }
  }, [toast, onScreenshot])

  const handleTimeUpdate = useCallback(() => {
    if (videoRef.current) {
      onTimeUpdate?.(videoRef.current.currentTime)
    }
  }, [onTimeUpdate])

  return (
    <Card className="w-full overflow-hidden">
      <CardContent className="p-0">
        <div className="relative">
          <video
            ref={videoRef}
            src={src}
            poster={poster}
            title={title}
            className="w-full aspect-video bg-black"
            controls
            onTimeUpdate={handleTimeUpdate}
            crossOrigin="anonymous"
          />

          <div className="absolute bottom-20 right-4 z-10">
            <Button
              variant="secondary"
              size="icon"
              onClick={handleScreenshot}
              className="shadow-lg hover:shadow-xl transition-shadow"
              title="Take Screenshot"
            >
              <Camera className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

function formatTimestamp(seconds: number): string {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)

  if (hours > 0) {
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}
