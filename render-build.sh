#!/usr/bin/env bash
set -e

echo "🛠️ Updating Python packages..."
python3 -m pip install --upgrade pip

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Build completed successfully!"
