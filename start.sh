#!/bin/bash

# METEORA LX - Quick Start Script for macOS/Linux
# This script starts both backend and frontend servers

set -e

echo "🎬 Starting METEORA LX..."
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Start backend
echo "📡 Starting backend server..."
cd backend

if [ ! -d "venv" ]; then
    echo "❌ Error: Python virtual environment not found"
    echo "Please run: cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

source venv/bin/activate
uvicorn app.main:app --reload --port 8000 > /tmp/meteora-backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
sleep 3

# Test backend
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "⚠️  Backend might not be ready yet"
fi

# Start frontend
echo ""
echo "🎨 Starting frontend server..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "❌ Error: Node modules not found"
    echo "Please run: cd frontend && npm install"
    kill $BACKEND_PID
    exit 1
fi

npm run dev > /tmp/meteora-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"

# Wait for frontend to be ready
sleep 3

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 METEORA LX is running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Frontend:  http://localhost:5173"
echo "🔌 Backend:   http://localhost:8000"
echo "📚 API Docs:  http://localhost:8000/docs"
echo ""
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "📋 Logs:"
echo "  Backend:  tail -f /tmp/meteora-backend.log"
echo "  Frontend: tail -f /tmp/meteora-frontend.log"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "✅ Servers stopped"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT TERM

# Wait for user to stop
wait
