import { Card, CardContent, CardHeader } from './ui/card'
import { cn } from '@/lib/utils'

/**
 * Skeleton component for loading states
 */
export function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn('animate-pulse rounded-md bg-muted', className)}
      {...props}
    />
  )
}

/**
 * Loading skeleton for video player
 */
export function VideoPlayerSkeleton() {
  return (
    <Card className="w-full overflow-hidden">
      <CardContent className="p-0">
        <div className="w-full aspect-video bg-muted relative">
          <div className="absolute inset-0 flex items-center justify-center">
            <Spinner size="lg" />
          </div>
          {/* Player controls skeleton */}
          <div className="absolute bottom-0 left-0 right-0 p-4 space-y-2">
            <Skeleton className="h-1 w-full" />
            <div className="flex items-center gap-2">
              <Skeleton className="h-8 w-8 rounded-full" />
              <Skeleton className="h-8 w-8 rounded-full" />
              <div className="flex-1" />
              <Skeleton className="h-8 w-8 rounded-full" />
              <Skeleton className="h-8 w-8 rounded-full" />
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

/**
 * Loading skeleton for upload UI
 */
export function UploadSkeleton() {
  return (
    <Card className="w-full">
      <CardHeader>
        <Skeleton className="h-6 w-32 mb-2" />
        <Skeleton className="h-4 w-64" />
      </CardHeader>
      <CardContent>
        <div className="border-2 border-dashed border-muted rounded-lg p-12 flex flex-col items-center justify-center space-y-4">
          <Spinner size="lg" />
          <Skeleton className="h-4 w-48" />
          <Skeleton className="h-4 w-32" />
        </div>
      </CardContent>
    </Card>
  )
}

/**
 * Loading skeleton for video list
 */
export function VideoListSkeleton() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 3 }).map((_, i) => (
        <Card key={i}>
          <CardContent className="p-4">
            <div className="flex gap-4">
              <Skeleton className="w-32 h-20 rounded" />
              <div className="flex-1 space-y-2">
                <Skeleton className="h-5 w-48" />
                <Skeleton className="h-4 w-32" />
                <Skeleton className="h-4 w-24" />
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

/**
 * General purpose spinner component
 */
export function Spinner({
  size = 'md',
  className,
}: {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}) {
  const sizeClasses = {
    sm: 'h-4 w-4 border-2',
    md: 'h-8 w-8 border-2',
    lg: 'h-12 w-12 border-3',
  }

  return (
    <div
      className={cn(
        'animate-spin rounded-full border-primary border-t-transparent',
        sizeClasses[size],
        className
      )}
      role="status"
      aria-label="Loading"
    >
      <span className="sr-only">Loading...</span>
    </div>
  )
}

/**
 * Full page loading screen
 */
export function LoadingScreen({ message = 'Loading...' }: { message?: string }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-background">
      <Spinner size="lg" />
      <p className="mt-4 text-muted-foreground">{message}</p>
    </div>
  )
}

/**
 * Card with loading state
 */
export function LoadingCard() {
  return (
    <Card>
      <CardContent className="p-8 flex flex-col items-center justify-center">
        <Spinner size="md" />
        <p className="mt-4 text-sm text-muted-foreground">Loading...</p>
      </CardContent>
    </Card>
  )
}
