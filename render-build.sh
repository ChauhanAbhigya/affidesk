#!/bin/bash
# --------------------------
# Update package lists (no sudo needed on Render)
# --------------------------
apt-get update -y

# --------------------------
# Install wkhtmltopdf and fontconfig (required for PDF generation)
# --------------------------
apt-get install -y wkhtmltopdf fontconfig

# --------------------------
# Install Python dependencies
# --------------------------
pip install --upgrade pip
pip install -r requirements.txt
