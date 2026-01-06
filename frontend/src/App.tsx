import { cn } from '@/lib/utils'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { VideoUploader } from '@/components/upload'
import { VideoPlayer } from '@/components/player'
import { Upload, PlayCircle } from 'lucide-react'

function App() {
  const [showUploader, setShowUploader] = useState(false)
  const [showPlayer, setShowPlayer] = useState(false)
  const [videoUrl, setVideoUrl] = useState<string>('')

  const handleUploadComplete = (videoId: string) => {
    console.log('Upload complete, video ID:', videoId)
    // In a real app, fetch the video stream URL from the backend
    // For now, we'll just show a success message
    setShowUploader(false)
  }

  const handleScreenshot = (_dataUrl: string, timestamp: number) => {
    console.log('Screenshot captured at', timestamp)
    // In a real app, save the screenshot to the backend
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="flex flex-col items-center justify-center min-h-screen p-8">
        <div className="max-w-4xl mx-auto w-full space-y-6">
          <div className="text-center space-y-4">
            <h1 className="text-6xl font-bold tracking-tight">
              METEORA <span className="text-primary">LX</span>
            </h1>
            <p className="text-xl text-muted-foreground">
              AI-Powered Movie Analysis Platform
            </p>
          </div>

          <div className={cn(
            "mt-8 p-6 rounded-lg border border-border",
            "bg-card shadow-cinematic"
          )}>
            <h2 className="text-2xl font-semibold mb-4">System Status</h2>
            <div className="space-y-2 text-left">
              <StatusItem label="Frontend Components" status="ready" />
              <StatusItem label="Video Upload (Uppy + TUS)" status="ready" />
              <StatusItem label="Video Player (Vidstack)" status="ready" />
              <StatusItem label="State Management (Zustand)" status="ready" />
              <StatusItem label="Backend API" status="pending" />
              <StatusItem label="Video Processing" status="pending" />
            </div>
          </div>

          <div className="flex gap-4 justify-center">
            <Button
              size="lg"
              onClick={() => {
                setShowUploader(!showUploader)
                setShowPlayer(false)
              }}
            >
              <Upload className="mr-2 h-5 w-5" />
              {showUploader ? 'Hide Uploader' : 'Show Uploader'}
            </Button>
            <Button
              size="lg"
              variant="outline"
              onClick={() => {
                setShowPlayer(!showPlayer)
                setShowUploader(false)
                // Demo video URL - in production this would come from the backend
                setVideoUrl('https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4')
              }}
            >
              <PlayCircle className="mr-2 h-5 w-5" />
              {showPlayer ? 'Hide Player' : 'Show Player Demo'}
            </Button>
          </div>

          {showUploader && (
            <div className="animate-in fade-in slide-in-from-bottom duration-300">
              <VideoUploader onUploadComplete={handleUploadComplete} />
            </div>
          )}

          {showPlayer && videoUrl && (
            <div className="animate-in fade-in slide-in-from-bottom duration-300">
              <VideoPlayer
                src={videoUrl}
                title="Demo Video"
                onScreenshot={handleScreenshot}
                onTimeUpdate={(time) => console.log('Time:', time)}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function StatusItem({ label, status }: { label: string; status: 'ready' | 'pending' | 'error' }) {
  const statusColors = {
    ready: 'text-green-500',
    pending: 'text-yellow-500',
    error: 'text-red-500',
  }

  const statusIcons = {
    ready: '●',
    pending: '○',
    error: '✕',
  }

  return (
    <div className="flex items-center justify-between p-3 rounded bg-secondary">
      <span className="font-medium">{label}</span>
      <span className={cn('font-mono text-sm', statusColors[status])}>
        {statusIcons[status]} {status.toUpperCase()}
      </span>
    </div>
  )
}

export default App
