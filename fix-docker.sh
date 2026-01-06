#!/bin/bash
# METEORA LX - Docker Module Resolution Fix Script
# Run this script to fix the "@/lib/utils" import error

set -e  # Exit on error

echo "🔧 METEORA LX - Fixing Docker Module Resolution"
echo "================================================"
echo ""

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed or not in PATH"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Determine which command to use
if command -v docker-compose &> /dev/null; then
    DC="docker-compose"
elif command -v docker &> /dev/null; then
    DC="docker compose"
else
    echo "❌ Error: Neither 'docker-compose' nor 'docker compose' found"
    exit 1
fi

echo "Using command: $DC"
echo ""

# Step 1: Stop containers
echo "📦 Step 1/5: Stopping containers..."
$DC down
echo "✅ Containers stopped"
echo ""

# Step 2: Remove frontend container and volume
echo "🗑️  Step 2/5: Removing old frontend container..."
$DC rm -f frontend 2>/dev/null || true
echo "✅ Old container removed"
echo ""

# Step 3: Clear Docker build cache for frontend
echo "🧹 Step 3/5: Clearing build cache..."
docker builder prune -f --filter "label=com.docker.compose.project=movie-summary" 2>/dev/null || true
echo "✅ Cache cleared"
echo ""

# Step 4: Rebuild frontend with no cache
echo "🔨 Step 4/5: Rebuilding frontend container (this may take a minute)..."
$DC build --no-cache frontend
echo "✅ Frontend rebuilt with latest configuration"
echo ""

# Step 5: Start all services
echo "🚀 Step 5/5: Starting all services..."
$DC up -d
echo "✅ All services started"
echo ""

# Wait a moment for services to initialize
echo "⏳ Waiting for services to initialize..."
sleep 5

# Check status
echo ""
echo "📊 Service Status:"
echo "=================="
$DC ps
echo ""

# Check frontend logs for errors
echo "📋 Frontend Logs (last 20 lines):"
echo "=================================="
$DC logs --tail=20 frontend
echo ""

# Check for the specific error
if $DC logs frontend 2>&1 | grep -q "Failed to resolve import"; then
    echo "⚠️  WARNING: Still seeing module resolution errors"
    echo ""
    echo "Try the nuclear option:"
    echo "  $DC down -v"
    echo "  $DC build --no-cache"
    echo "  $DC up -d"
    echo ""
else
    echo "✅ SUCCESS! No module resolution errors detected"
    echo ""
    echo "🎉 METEORA LX is ready!"
    echo ""
    echo "Access the application:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend:  http://localhost:8000"
    echo "  API Docs: http://localhost:8000/docs"
    echo ""
    echo "Monitor logs:"
    echo "  $DC logs -f frontend"
    echo "  $DC logs -f backend"
fi

echo ""
echo "================================================"
echo "Fix script completed!"
