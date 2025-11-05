@echo off
REM CodeForge AI - Run Script for Windows
REM This script sets up and runs the CodeForge AI application

echo 🔥 CodeForge AI - Starting...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
if not exist "venv\installed.flag" (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
    echo. > venv\installed.flag
) else (
    echo ✅ Dependencies already installed
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  No .env file found!
    echo 📋 Copying .env.example to .env...
    copy .env.example .env
    echo.
    echo ❗ IMPORTANT: Edit .env and add your ANTHROPIC_API_KEY
    echo    Get your API key from: https://console.anthropic.com/
    echo.
    pause
)

REM Create required directories
echo 📁 Creating directories...
if not exist "generated_projects" mkdir generated_projects
if not exist "logs" mkdir logs

REM Run the application
echo.
echo 🚀 Starting CodeForge AI...
echo 🌐 Open your browser to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
