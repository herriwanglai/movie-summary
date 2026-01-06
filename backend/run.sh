#!/bin/bash

# METEORA LX Backend Startup Script

echo "Starting METEORA LX Backend API..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Start server
echo "Starting Uvicorn server on http://0.0.0.0:8000"
echo "API Documentation available at http://localhost:8000/docs"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
