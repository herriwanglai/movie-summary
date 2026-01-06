#!/bin/bash
# Quick restart - try this first before rebuilding

echo "🔄 Quick Restart of Frontend Container"
echo "======================================="
echo ""

# Determine docker compose command
if command -v docker-compose &> /dev/null; then
    DC="docker-compose"
elif command -v docker &> /dev/null; then
    DC="docker compose"
else
    echo "❌ Docker not found"
    exit 1
fi

echo "1. Restarting frontend container..."
$DC restart frontend

echo ""
echo "2. Waiting for restart..."
sleep 3

echo ""
echo "3. Checking logs..."
$DC logs --tail=30 frontend

echo ""
if $DC logs frontend 2>&1 | grep -q "Failed to resolve import"; then
    echo "❌ Still seeing errors - need full rebuild"
    echo ""
    echo "Run this instead:"
    echo "  ./fix-docker.sh"
    exit 1
else
    echo "✅ No errors! Frontend should be working now"
    echo ""
    echo "Access at: http://localhost:3000"
fi
