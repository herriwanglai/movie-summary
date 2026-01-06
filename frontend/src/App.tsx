import { cn } from '@/lib/utils'

function App() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="flex flex-col items-center justify-center min-h-screen p-8">
        <div className="max-w-4xl mx-auto text-center space-y-6">
          <h1 className="text-6xl font-bold tracking-tight">
            METEORA <span className="text-primary">LX</span>
          </h1>
          <p className="text-xl text-muted-foreground">
            AI-Powered Movie Analysis Platform
          </p>
          <div className={cn(
            "mt-8 p-6 rounded-lg border border-border",
            "bg-card shadow-cinematic"
          )}>
            <h2 className="text-2xl font-semibold mb-4">System Status</h2>
            <div className="space-y-2 text-left">
              <StatusItem label="Frontend" status="ready" />
              <StatusItem label="Backend API" status="pending" />
              <StatusItem label="Video Processing" status="pending" />
              <StatusItem label="Ollama Integration" status="pending" />
            </div>
          </div>
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
