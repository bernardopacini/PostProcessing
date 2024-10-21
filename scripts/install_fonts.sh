#!/bin/bash

fonts="https://font.download/dl/font/cmu-bright.zip"

# Function to install fonts on Linux (System-wide)
install_fonts_linux() {
    echo "Installing fonts on Linux..."
    sudo mkdir -p /usr/share/fonts/truetype/cmu-bright
    sudo mv font/*.ttf /usr/share/fonts/truetype/cmu-bright/
    sudo chmod 644 /usr/share/fonts/truetype/cmu-bright/*.ttf
    sudo fc-cache -f -v /usr/share/fonts/truetype/cmu-bright
}

# Function to install fonts on macOS
install_fonts_macos() {
    echo "Installing fonts on macOS..."
    mkdir -p ~/Library/Fonts
    mv font/*.ttf ~/Library/Fonts/
}

# Download and unzip the font
download_and_extract_fonts() {
    for font in $fonts; do
        curl -L -o font.zip $font
        unzip font.zip -d font
        rm font.zip
    done
}

# Detect the operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    download_and_extract_fonts
    install_fonts_linux
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    download_and_extract_fonts
    install_fonts_macos
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

# Clean up
rm -rf font
