#!/usr/bin/env bash

# Exit immediately if a command fails
set -e

echo "🛠️ Updating system packages..."
sudo apt-get update -y

echo "📦 Installing wkhtmltopdf for PDF generation..."
sudo apt-get install -y wkhtmltopdf

echo "🖋️ Installing Hindi fonts (Noto Sans Devanagari)..."
sudo apt-get install -y fonts-noto fonts-noto-cjk fonts-noto-hinted fonts-noto-unhinted fonts-noto-ui-core
sudo fc-cache -f -v

echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Render build completed successfully!"
