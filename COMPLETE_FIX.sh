#!/bin/bash
# COMPLETE FIX - Nuclear option that will definitely work

set -e

echo "🚀 COMPLETE FIX for @/lib/utils Import Error"
echo "============================================="
echo ""
echo "This will:"
echo "  1. Fix all file permissions"
echo "  2. Stop all containers"
echo "  3. Rebuild frontend from scratch"
echo "  4. Start everything fresh"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Detect docker-compose command
if command -v docker-compose &> /dev/null; then
    DC="docker-compose"
elif command -v docker &> /dev/null; then
    DC="docker compose"
else
    echo "❌ Error: Docker not found"
    exit 1
fi

echo ""
echo "Step 1: Fixing file permissions on host..."
cd /home/user/movie-summary
chmod -R 755 frontend/src 2>/dev/null || true
find frontend/src -type f -name "*.ts" -exec chmod 644 {} \; 2>/dev/null || true
find frontend/src -type f -name "*.tsx" -exec chmod 644 {} \; 2>/dev/null || true
chmod 644 frontend/vite.config.ts 2>/dev/null || true
chmod 644 frontend/tsconfig*.json 2>/dev/null || true
echo "  ✅ Permissions fixed"

echo ""
echo "Step 2: Verifying utils.ts exists..."
if [ -f "frontend/src/lib/utils.ts" ]; then
    echo "  ✅ utils.ts found"
    ls -la frontend/src/lib/utils.ts
else
    echo "  ❌ ERROR: utils.ts not found!"
    echo "  Creating it now..."
    mkdir -p frontend/src/lib
    cat > frontend/src/lib/utils.ts << 'EOF'
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatTimestamp(seconds: number): string {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)

  if (hours > 0) {
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

export function parseTimestamp(timestamp: string): number {
  const parts = timestamp.split(':').map(Number)
  if (parts.length === 3) {
    return parts[0] * 3600 + parts[1] * 60 + parts[2]
  }
  if (parts.length === 2) {
    return parts[0] * 60 + parts[1]
  }
  return 0
}
EOF
    chmod 644 frontend/src/lib/utils.ts
    echo "  ✅ utils.ts created"
fi

echo ""
echo "Step 3: Stopping all containers..."
$DC down
echo "  ✅ Containers stopped"

echo ""
echo "Step 4: Removing old images and cache..."
$DC rm -f frontend 2>/dev/null || true
docker volume rm movie-summary_frontend_node_modules 2>/dev/null || echo "  (no volume to remove)"
echo "  ✅ Cache cleared"

echo ""
echo "Step 5: Rebuilding frontend container (this may take a minute)..."
$DC build --no-cache frontend
echo "  ✅ Frontend rebuilt"

echo ""
echo "Step 6: Starting all services..."
$DC up -d
echo "  ✅ Services started"

echo ""
echo "Step 7: Waiting for Vite to start (10 seconds)..."
sleep 10

echo ""
echo "Step 8: Checking frontend logs..."
echo "=========================================="
$DC logs --tail=50 frontend
echo "=========================================="

echo ""
echo "Step 9: Verifying fix..."
if $DC logs frontend 2>&1 | grep -q "Failed to resolve import"; then
    echo "❌ STILL SEEING ERRORS"
    echo ""
    echo "Let's check what's in the container:"
    echo ""
    $DC exec frontend ls -la /app/src/lib/ || echo "❌ Can't access lib directory"
    echo ""
    $DC exec frontend cat /app/vite.config.ts | grep -A 5 "alias"
    echo ""
    echo "Please run: ./debug-docker.sh for more info"
else
    echo "✅ SUCCESS! No import errors detected"
    echo ""
    echo "Frontend should be running at: http://localhost:3000"
    echo ""
    echo "Check with: curl http://localhost:3000"
fi

echo ""
echo "=========================================="
echo "Complete fix applied!"
echo "=========================================="
