#!/bin/bash
# Debug script to check what's happening inside Docker container

echo "🔍 Debugging Docker Container File System"
echo "=========================================="
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

echo "1. Checking if lib directory exists in container..."
$DC exec frontend ls -la /app/src/lib/ || echo "❌ lib directory not found in container!"

echo ""
echo "2. Checking if utils.ts exists in container..."
$DC exec frontend cat /app/src/lib/utils.ts | head -5 || echo "❌ utils.ts not found or not readable!"

echo ""
echo "3. Checking file permissions in container..."
$DC exec frontend ls -la /app/src/lib/

echo ""
echo "4. Checking vite.config.ts in container..."
$DC exec frontend cat /app/vite.config.ts

echo ""
echo "5. Checking tsconfig.app.json in container..."
$DC exec frontend cat /app/tsconfig.app.json | grep -A 5 "paths"

echo ""
echo "6. Testing path resolution in container..."
$DC exec frontend node -e "const path = require('path'); console.log('Resolved @:', path.resolve('/app', 'src'));"

echo ""
echo "=========================================="
