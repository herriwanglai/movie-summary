#!/bin/bash
# Diagnostic script to check Docker container state

echo "🔍 Docker Container Diagnostics"
echo "================================"
echo ""

DC="docker-compose"
if ! command -v docker-compose &> /dev/null; then
    DC="docker compose"
fi

echo "1. Checking if utils.ts exists in container..."
$DC exec frontend ls -la /app/src/lib/utils.ts
echo ""

echo "2. Checking vite.config.ts in container..."
$DC exec frontend cat /app/vite.config.ts
echo ""

echo "3. Checking tsconfig.app.json in container..."
$DC exec frontend cat /app/tsconfig.app.json
echo ""

echo "4. Checking if vite can see the src directory..."
$DC exec frontend ls -la /app/src/lib/
echo ""

echo "5. Checking node version..."
$DC exec frontend node --version
echo ""

echo "6. Checking working directory..."
$DC exec frontend pwd
echo ""

echo "7. Testing path resolution..."
$DC exec frontend node -e "const path = require('path'); console.log('__dirname:', __dirname); console.log('resolved:', path.resolve(__dirname, './src'));"
echo ""

echo "8. Checking if @ alias is in vite config..."
$DC exec frontend grep -A 2 "alias" /app/vite.config.ts
echo ""

echo "9. Recent frontend logs..."
$DC logs --tail=50 frontend
