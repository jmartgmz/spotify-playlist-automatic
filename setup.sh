#!/bin/bash
# setup.sh - Setup script for Spotify Playlist Automatic Downloader
# This script creates a virtual environment, installs dependencies, and prompts for configuration

set -e  # Exit on any error

echo "=========================================="
echo "Spotify Playlist Automatic Downloader Setup"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install it first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "Setting up .env file..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ Created .env from template"
        echo ""
        echo "Please edit .env and add your Spotify credentials:"
        echo "  - SPOTIFY_CLIENT_ID"
        echo "  - SPOTIFY_CLIENT_SECRET"
        echo "  - SPOTIFY_REDIRECT_URI (optional, defaults to http://127.0.0.1:8888/callback)"
        echo ""
    fi
else
    echo "✓ .env file already exists"
fi

# Check if playlists.txt exists
if [ ! -f "playlists.txt" ]; then
    echo ""
    echo "Creating playlists.txt..."
    cat > playlists.txt << 'EOF'
# Add your Spotify playlist URLs or IDs below, one per line
# Lines starting with # are comments
# Example:
# https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
EOF
    echo "✓ Created playlists.txt"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env with your Spotify API credentials"
echo "2. Edit playlists.txt with your playlist URLs"
echo "3. Activate the environment: source .venv/bin/activate"
echo "4. Run commands:"
echo "   python src/update_playlists_txt.py  # Auto-discover playlists"
echo "   python src/check.py                 # One-time check"
echo "   python src/watch.py                 # Continuous watcher"
echo ""
echo "For more info, see README.md"
echo ""
