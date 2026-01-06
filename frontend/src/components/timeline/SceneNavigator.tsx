import { useTimelineStore } from '@/stores/timelineStore'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Film, ChevronLeft, ChevronRight } from 'lucide-react'
import { cn } from '@/lib/utils'

export function SceneNavigator() {
  const {
    scenes,
    currentTime,
    selectedSceneId,
    jumpToScene,
    previousScene,
    nextScene,
  } = useTimelineStore()

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const formatDuration = (seconds: number): string => {
    if (seconds < 60) {
      return `${seconds.toFixed(1)}s`
    }
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}m ${secs}s`
  }

  const currentScene = scenes.find(
    (scene) => currentTime >= scene.start_time && currentTime <= scene.end_time
  )

  if (scenes.length === 0) {
    return (
      <Card className="p-4 bg-gray-900/30 border-gray-800">
        <div className="flex flex-col items-center justify-center text-center gap-2 py-4">
          <Film className="h-8 w-8 text-gray-600" />
          <p className="text-sm text-gray-500">No scenes detected yet</p>
        </div>
      </Card>
    )
  }

  return (
    <div className="space-y-3">
      {/* Current Scene Info */}
      {currentScene && (
        <Card className="p-4 bg-gradient-to-r from-blue-500/10 to-purple-500/10 border-blue-500/30">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-semibold text-blue-400">Current Scene</h3>
            <span className="text-xs text-gray-400">
              {scenes.indexOf(currentScene) + 1} of {scenes.length}
            </span>
          </div>
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={previousScene}
              disabled={scenes.indexOf(currentScene) === 0}
              className="hover:bg-gray-800"
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <div className="flex-1">
              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-bold text-white">
                  Scene {scenes.indexOf(currentScene) + 1}
                </span>
                <span className="text-xs text-gray-500">
                  {formatDuration(currentScene.duration)}
                </span>
              </div>
              <div className="text-xs text-gray-400 mt-1">
                {formatTime(currentScene.start_time)} → {formatTime(currentScene.end_time)}
              </div>
              {currentScene.keyframe_count > 0 && (
                <div className="text-xs text-green-400 mt-1">
                  {currentScene.keyframe_count} keyframes
                </div>
              )}
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={nextScene}
              disabled={scenes.indexOf(currentScene) === scenes.length - 1}
              className="hover:bg-gray-800"
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </Card>
      )}

      {/* Scene List */}
      <Card className="p-3 bg-gray-900/30 border-gray-800 max-h-64 overflow-y-auto">
        <h3 className="text-xs font-semibold text-gray-400 mb-2 px-1">All Scenes</h3>
        <div className="space-y-1">
          {scenes.map((scene, index) => {
            const isSelected = selectedSceneId === scene.id
            const isCurrent = currentScene?.id === scene.id

            return (
              <button
                key={scene.id}
                onClick={() => jumpToScene(scene.id)}
                className={cn(
                  'w-full text-left px-3 py-2 rounded transition-colors',
                  'hover:bg-gray-800/50',
                  isCurrent && 'bg-blue-500/20 border border-blue-500/30',
                  isSelected && !isCurrent && 'bg-gray-800/30'
                )}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Film className={cn(
                      'h-3 w-3',
                      isCurrent ? 'text-blue-400' : 'text-gray-600'
                    )} />
                    <span className={cn(
                      'text-sm font-medium',
                      isCurrent ? 'text-white' : 'text-gray-300'
                    )}>
                      Scene {index + 1}
                    </span>
                  </div>
                  <span className="text-xs text-gray-500">
                    {formatDuration(scene.duration)}
                  </span>
                </div>
                <div className="flex items-center justify-between mt-1">
                  <span className="text-[10px] text-gray-600">
                    {formatTime(scene.start_time)} - {formatTime(scene.end_time)}
                  </span>
                  {scene.keyframe_count > 0 && (
                    <span className="text-[10px] text-green-600">
                      {scene.keyframe_count} keyframes
                    </span>
                  )}
                </div>
              </button>
            )
          })}
        </div>
      </Card>
    </div>
  )
}
