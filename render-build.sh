#!/usr/bin/env bash
# Install dependencies on Render
apt-get update && apt-get install -y \
    wkhtmltopdf \
    fonts-lohit-deva \
    fonts-noto-core \
    fonts-noto-unhinted \
    fonts-noto-cjk \
    fonts-noto-color-emoji

pip install -r requirements.txt
