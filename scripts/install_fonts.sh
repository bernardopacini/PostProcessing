#!/bin/bash

fonts=("https://font.download/dl/font/cmu-bright.zip" "https://font.download/dl/font/open-sans.zip")

# Function to install fonts on Linux (System-wide)
install_fonts_linux() {
    echo "Installing fonts on Linux..."
    for font in "${fonts[@]}"; do
        font_name=$(basename "$font" .zip)
        mkdir -p "$HOME/.local/share/fonts/$font_name"
        mv "font/$font_name/"*.ttf "$HOME/.local/share/fonts/$font_name/"
        sudo ln -s "$HOME/.local/share/fonts/$font_name" "/usr/share/fonts/truetype/$font_name"
    done
    fc-cache -f -v
}

# Function to install fonts on macOS
install_fonts_macos() {
    echo "Installing fonts on macOS..."
    for font in "${fonts[@]}"; do
        font_name=$(basename "$font" .zip)
        mkdir -p ~/Library/Fonts
        mv "font/$font_name/"*.ttf ~/Library/Fonts/
    done
}

# Download and unzip the fonts
download_and_extract_fonts() {
    for font in "${fonts[@]}"; do
        font_name=$(basename "$font" .zip)
        mkdir -p "font/$font_name"
        curl -L -o "$font_name.zip" "$font"
        unzip -q "$font_name.zip" -d "font/$font_name"
        rm "$font_name.zip"
    done
}

# Detect the operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    mkdir -p font
    download_and_extract_fonts
    install_fonts_linux
elif [[ "$OSTYPE" == "darwin"* ]]; then
    mkdir -p font
    download_and_extract_fonts
    install_fonts_macos
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

# Clean up
rm -rf font
