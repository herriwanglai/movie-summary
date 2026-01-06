#!/bin/bash
# IMMEDIATE FIX for @/lib/utils import error
# This script will actually fix the running Docker container

set -e

echo "🔧 FIXING @/lib/utils Import Error in Docker"
echo "=============================================="
echo ""

# Detect docker-compose command
if command -v docker-compose &> /dev/null; then
    DC="docker-compose"
elif command -v docker &> /dev/null; then
    DC="docker compose"
else
    echo "❌ Error: Docker not found"
    exit 1
fi

echo "Step 1: Stopping frontend container..."
$DC stop frontend || true

echo ""
echo "Step 2: Removing frontend container to clear cache..."
$DC rm -f frontend || true

echo ""
echo "Step 3: Clearing Vite cache in volume..."
$DC run --rm frontend sh -c "rm -rf /app/node_modules/.vite" || true

echo ""
echo "Step 4: Starting frontend with fresh state..."
$DC up -d frontend

echo ""
echo "Step 5: Waiting for Vite to start..."
sleep 5

echo ""
echo "Step 6: Checking logs for errors..."
$DC logs --tail=30 frontend

echo ""
echo "=========================================="
echo "✅ Fix applied! Check logs above for success"
echo ""
echo "If you still see errors, try full rebuild:"
echo "  $DC down"
echo "  $DC build --no-cache frontend"
echo "  $DC up -d"
