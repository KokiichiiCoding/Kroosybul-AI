#!/bin/bash

# Kroosybul AI - Run Script
# This script sets up and runs the Kroosybul AI application

set -e

echo "🔥 Kroosybul AI - Starting..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/installed.flag" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/installed.flag
else
    echo "✅ Dependencies already installed"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo "📋 Copying .env.example to .env..."
    cp .env.example .env
    echo ""
    echo "❗ IMPORTANT: Edit .env and add your ANTHROPIC_API_KEY"
    echo "   Get your API key from: https://console.anthropic.com/"
    echo ""
    read -p "Press Enter after you've added your API key to .env..."
fi

# Create required directories
echo "📁 Creating directories..."
mkdir -p generated_projects
mkdir -p logs

# Run the application
echo ""
echo "🚀 Starting Kroosybul AI..."
echo "🌐 Open your browser to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
