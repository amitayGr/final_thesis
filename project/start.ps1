# Startup Script for Integrated Geometry Learning System
# This script starts both backend and frontend services

Write-Host "🚀 Starting Integrated Geometry Learning System" -ForegroundColor Green
Write-Host "=" -Repeat 60 -ForegroundColor Gray

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Function to start a service in a new window
function Start-Service {
    param(
        [string]$ServiceName,
        [string]$ServicePath,
        [string]$Color
    )
    
    Write-Host "🔄 Starting $ServiceName..." -ForegroundColor $Color
    
    if (Test-Path "$ServicePath\app.py") {
        $command = "cd '$ServicePath'; python app.py"
        Start-Process powershell -ArgumentList "-NoExit", "-Command", $command
        Write-Host "✅ $ServiceName started in new window" -ForegroundColor Green
    } else {
        Write-Host "❌ app.py not found in $ServicePath" -ForegroundColor Red
        return $false
    }
    
    return $true
}

# Start Backend Service
$backendPath = Join-Path $projectRoot "backend_service"
$backendStarted = Start-Service -ServiceName "Backend Service" -ServicePath $backendPath -Color "Cyan"

if (-not $backendStarted) {
    Write-Host "Failed to start Backend Service" -ForegroundColor Red
    exit 1
}

# Wait a moment for backend to initialize
Write-Host "⏳ Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start Frontend Service
$frontendPath = Join-Path $projectRoot "frontend_service"
$frontendStarted = Start-Service -ServiceName "Frontend Service" -ServicePath $frontendPath -Color "Magenta"

if (-not $frontendStarted) {
    Write-Host "Failed to start Frontend Service" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=" -Repeat 60 -ForegroundColor Gray
Write-Host "✅ Both services started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access Points:" -ForegroundColor Yellow
Write-Host "   Frontend: http://localhost:5000" -ForegroundColor Cyan
Write-Host "   Backend:  http://localhost:5001/api/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Logs:" -ForegroundColor Yellow
Write-Host "   Backend:  $projectRoot\logs\backend_service.log" -ForegroundColor Gray
Write-Host "   Frontend: $projectRoot\logs\frontend_service.log" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  To stop the services, close both PowerShell windows" -ForegroundColor Yellow
Write-Host "=" -Repeat 60 -ForegroundColor Gray

# Wait for user input
Write-Host ""
Write-Host "Press any key to open the application in your browser..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open browser
Start-Process "http://localhost:5000"

Write-Host "🌐 Browser opened. The application should load shortly." -ForegroundColor Green
Write-Host "If nothing appears, wait a few seconds and refresh the page." -ForegroundColor Yellow
