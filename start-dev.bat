@echo off
REM ElfAgent Development Startup Script for Windows

echo 🎄 Starting ElfAgent Development Environment...

REM Check if backend .env exists
if not exist "backend\app\.env" (
    echo ⚠️  Warning: backend\app\.env not found
    echo 📝 Creating from example...
    if exist "backend\app\.env.example" (
        copy "backend\app\.env.example" "backend\app\.env"
        echo ✅ Created backend\app\.env - Please edit with your API keys
        exit /b 1
    ) else (
        echo ❌ backend\app\.env.example not found
        exit /b 1
    )
)

echo 🚀 Starting backend API...
start "ElfAgent Backend" cmd /k "cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo ⏳ Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

echo 🚀 Starting frontend...
start "ElfAgent Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ✅ ElfAgent is running!
echo 📡 Backend API: http://localhost:8000
echo 📡 API Docs: http://localhost:8000/docs
echo 🌐 Frontend: http://localhost:3000
echo.
echo Close the terminal windows to stop the services
