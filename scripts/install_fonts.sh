#!/bin/bash

fonts="https://font.download/dl/font/cmu-bright.zip"

# Function to install fonts on Linux
install_fonts_linux() {
    echo "Installing fonts on Linux..."
    mkdir -p ~/.local/share/fonts
    mv font/*.ttf ~/.local/share/fonts/
    fc-cache -f -v ~/.local/share/fonts
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
