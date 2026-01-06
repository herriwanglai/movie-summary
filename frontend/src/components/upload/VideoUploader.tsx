import { useState, useRef, type ChangeEvent, type DragEvent } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { useToast } from '@/hooks/use-toast'
import { Upload, X, Film } from 'lucide-react'
import { cn } from '@/lib/utils'

interface VideoUploaderProps {
  onUploadComplete?: (videoId: string) => void
  onUploadProgress?: (progress: number) => void
}

export function VideoUploader({ onUploadComplete, onUploadProgress }: VideoUploaderProps) {
  const { toast } = useToast()
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (file: File) => {
    // Validate file type
    if (!file.type.startsWith('video/')) {
      toast({
        variant: 'destructive',
        title: 'Invalid file type',
        description: 'Please select a video file',
      })
      return
    }

    // Validate file size (10GB max)
    const maxSize = 10 * 1024 * 1024 * 1024
    if (file.size > maxSize) {
      toast({
        variant: 'destructive',
        title: 'File too large',
        description: 'Maximum file size is 10GB',
      })
      return
    }

    setSelectedFile(file)
    toast({
      title: 'File selected',
      description: `${file.name} ready to upload`,
    })
  }

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      handleFileSelect(file)
    }
  }

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(false)

    const file = e.dataTransfer.files?.[0]
    if (file) {
      handleFileSelect(file)
    }
  }

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleUpload = async () => {
    if (!selectedFile) return

    setUploading(true)
    setProgress(0)

    try {
      // Simulate upload progress (replace with actual TUS upload when backend is ready)
      const formData = new FormData()
      formData.append('video', selectedFile)

      // Simulate progress
      const interval = setInterval(() => {
        setProgress((prev) => {
          const next = prev + 10
          onUploadProgress?.(next)
          if (next >= 100) {
            clearInterval(interval)
          }
          return next
        })
      }, 500)

      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 5000))

      clearInterval(interval)
      setProgress(100)

      toast({
        title: 'Upload successful',
        description: 'Your video is now being processed',
      })

      onUploadComplete?.('demo-video-id')

      // Reset state
      setTimeout(() => {
        setSelectedFile(null)
        setProgress(0)
        setUploading(false)
      }, 1000)
    } catch (error) {
      console.error('Upload error:', error)
      toast({
        variant: 'destructive',
        title: 'Upload failed',
        description: error instanceof Error ? error.message : 'Unknown error',
      })
      setUploading(false)
      setProgress(0)
    }
  }

  const handleClear = () => {
    setSelectedFile(null)
    setProgress(0)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
    if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
    return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB'
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Upload Video</CardTitle>
        <CardDescription>
          Upload a video file for AI-powered analysis. Supports files up to 10GB.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          className={cn(
            'border-2 border-dashed rounded-lg p-8 transition-colors',
            isDragging
              ? 'border-primary bg-primary/10'
              : 'border-border hover:border-primary/50',
            uploading && 'pointer-events-none opacity-50'
          )}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="video/*"
            onChange={handleFileChange}
            className="hidden"
            disabled={uploading}
          />

          {!selectedFile ? (
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <Upload className="h-12 w-12 text-muted-foreground" />
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground">
                  Drag and drop your video here, or
                </p>
                <Button
                  onClick={() => fileInputRef.current?.click()}
                  variant="outline"
                  disabled={uploading}
                >
                  Browse Files
                </Button>
              </div>
              <p className="text-xs text-muted-foreground">
                MP4, MOV, AVI, MKV up to 10GB
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <Film className="h-8 w-8 text-primary flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="font-medium truncate">{selectedFile.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {formatFileSize(selectedFile.size)}
                  </p>
                </div>
                {!uploading && (
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={handleClear}
                    className="flex-shrink-0"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                )}
              </div>

              {uploading && (
                <div className="space-y-2">
                  <Progress value={progress} />
                  <p className="text-xs text-muted-foreground text-center">
                    Uploading... {progress}%
                  </p>
                </div>
              )}

              {!uploading && (
                <Button onClick={handleUpload} className="w-full" size="lg">
                  <Upload className="mr-2 h-4 w-4" />
                  Upload Video
                </Button>
              )}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
