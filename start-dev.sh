#!/bin/bash

# ElfAgent Development Startup Script

echo "🎄 Starting ElfAgent Development Environment..."

# Check if backend .env exists
if [ ! -f "backend/app/.env" ]; then
    echo "⚠️  Warning: backend/app/.env not found"
    echo "📝 Creating from example..."
    if [ -f "backend/app/.env.example" ]; then
        cp backend/app/.env.example backend/app/.env
        echo "✅ Created backend/app/.env - Please edit with your API keys"
        exit 1
    else
        echo "❌ backend/app/.env.example not found"
        exit 1
    fi
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend
echo "🚀 Starting backend API..."
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Start frontend
echo "🚀 Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ ElfAgent is running!"
echo "📡 Backend API: http://localhost:8000"
echo "📡 API Docs: http://localhost:8000/docs"
echo "🌐 Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for processes
wait
