#!/bin/bash
apt-get update && apt-get install -y \
    wkhtmltopdf \
    xfonts-75dpi \
    xfonts-base \
    fonts-noto \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    fonts-deva

pip install -r requirements.txt
