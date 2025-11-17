#!/bin/bash
# AncesTree Installer for macOS
# This script installs Docker Desktop and sets up AncesTree

set -e

echo "========================================"
echo "AncesTree Installer for macOS"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}ERROR: This script is for macOS only${NC}"
    exit 1
fi

# Detect architecture
ARCH=$(uname -m)
if [[ "$ARCH" == "arm64" ]]; then
    DOCKER_URL="https://desktop.docker.com/mac/main/arm64/Docker.dmg"
    echo "Detected: Apple Silicon (M1/M2/M3)"
elif [[ "$ARCH" == "x86_64" ]]; then
    DOCKER_URL="https://desktop.docker.com/mac/main/amd64/Docker.dmg"
    echo "Detected: Intel Mac"
else
    echo -e "${RED}ERROR: Unknown architecture: $ARCH${NC}"
    exit 1
fi
echo

# Check if Docker is already installed
if command -v docker &> /dev/null; then
    echo -e "${GREEN}[✓] Docker is already installed${NC}"
    docker --version
    echo

    # Check if Docker is running
    if docker ps &> /dev/null; then
        echo -e "${GREEN}Docker is running!${NC}"
        echo
        read -p "Would you like to start AncesTree now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cd "$(dirname "$0")/.."
            python3 scripts/launcher.py
        fi
        exit 0
    else
        echo -e "${YELLOW}Docker is installed but not running.${NC}"
        echo
        echo "Please start Docker Desktop from Applications,"
        echo "then run: ./scripts/start_ancestree.sh"
        exit 0
    fi
fi

echo "[1/5] Docker not found. Installing Docker Desktop..."
echo

# Create temp directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo "[2/5] Downloading Docker Desktop..."
echo "This may take several minutes (approximately 600 MB)..."
echo

# Download Docker Desktop
if ! curl -L -o "$TEMP_DIR/Docker.dmg" "$DOCKER_URL" --progress-bar; then
    echo -e "${RED}ERROR: Failed to download Docker Desktop${NC}"
    echo
    echo "Please download manually from:"
    echo "https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo
echo -e "${GREEN}[✓] Download complete${NC}"
echo

echo "[3/5] Mounting disk image..."
MOUNT_DIR=$(hdiutil attach "$TEMP_DIR/Docker.dmg" | grep Volumes | awk '{print $3}')

if [ -z "$MOUNT_DIR" ]; then
    echo -e "${RED}ERROR: Failed to mount Docker disk image${NC}"
    exit 1
fi

echo "[4/5] Installing Docker Desktop..."
echo

# Copy Docker to Applications
echo "Copying Docker.app to /Applications..."
if [ -d "/Applications/Docker.app" ]; then
    echo "Removing old Docker.app..."
    rm -rf "/Applications/Docker.app"
fi

cp -R "$MOUNT_DIR/Docker.app" /Applications/

echo
echo -e "${GREEN}[✓] Docker.app installed to /Applications${NC}"
echo

echo "[5/5] Cleaning up..."
hdiutil detach "$MOUNT_DIR" -quiet
rm -rf "$TEMP_DIR"

echo
echo "========================================"
echo "Docker Desktop Installation Complete!"
echo "========================================"
echo
echo -e "${GREEN}NEXT STEPS:${NC}"
echo
echo "1. ${YELLOW}OPEN DOCKER DESKTOP${NC} from Applications"
echo "   - Look for Docker.app in your Applications folder"
echo "   - Double-click to launch"
echo
echo "2. ${YELLOW}FIRST TIME SETUP${NC}"
echo "   - Accept the terms and conditions"
echo "   - Docker may ask for your password (for privileged access)"
echo "   - Wait for Docker to start (whale icon in menu bar)"
echo "   - Initial startup may take 2-3 minutes"
echo
echo "3. ${YELLOW}START ANCESTREE${NC}"
echo "   - Option 1: Double-click scripts/Start AncesTree.command"
echo "   - Option 2: Run ./scripts/start_ancestree.sh"
echo "   - Option 3: Run python3 scripts/launcher.py"
echo
echo "For help, see: docs/USER_GUIDE.md"
echo
echo "Press Enter to open Docker Desktop now, or Ctrl+C to exit"
read

# Open Docker Desktop
open /Applications/Docker.app

echo
echo "Waiting for Docker to start..."
echo "(This may take 1-2 minutes on first launch)"
echo

# Wait for Docker to be ready
for i in {1..60}; do
    if docker ps &> /dev/null; then
        echo
        echo -e "${GREEN}[✓] Docker is ready!${NC}"
        echo

        read -p "Would you like to start AncesTree now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cd "$(dirname "$0")/.."
            python3 scripts/launcher.py
        fi
        exit 0
    fi
    sleep 2
    echo -n "."
done

echo
echo -e "${YELLOW}Docker is taking longer than expected to start.${NC}"
echo
echo "Please wait for Docker to finish starting, then run:"
echo "  ./scripts/start_ancestree.sh"
echo
