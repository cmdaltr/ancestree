#!/bin/bash
# AncesTree Installer for Linux
# This script installs Docker and sets up AncesTree

set -e

echo "========================================"
echo "AncesTree Installer for Linux"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}ERROR: This script is for Linux only${NC}"
    exit 1
fi

# Detect distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
    VERSION=$VERSION_ID
else
    echo -e "${RED}ERROR: Cannot detect Linux distribution${NC}"
    exit 1
fi

echo "Detected: $PRETTY_NAME"
echo

# Check if Docker is already installed
if command -v docker &> /dev/null; then
    echo -e "${GREEN}[✓] Docker is already installed${NC}"
    docker --version
    echo

    # Check if Docker daemon is running
    if sudo docker ps &> /dev/null; then
        echo -e "${GREEN}Docker is running!${NC}"
        echo

        # Check if user is in docker group
        if groups | grep -q docker; then
            echo -e "${GREEN}User is in docker group${NC}"
            START_CMD="./scripts/start_ancestree.sh"
        else
            echo -e "${YELLOW}Note: You are not in the docker group${NC}"
            echo "You can run docker commands with sudo"
            START_CMD="sudo ./scripts/start_ancestree.sh"
        fi

        echo
        read -p "Would you like to start AncesTree now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cd "$(dirname "$0")/.."
            if groups | grep -q docker; then
                python3 scripts/launcher.py
            else
                sudo python3 scripts/launcher.py
            fi
        fi
        exit 0
    else
        echo -e "${YELLOW}Docker is installed but not running${NC}"
        echo
        echo "Starting Docker daemon..."
        sudo systemctl start docker
        sleep 2
        echo -e "${GREEN}Docker started${NC}"
        exit 0
    fi
fi

echo "[1/4] Docker not found. Installing Docker..."
echo

# Function to install Docker on Ubuntu/Debian
install_docker_debian() {
    echo "Installing Docker on Debian/Ubuntu..."

    # Update package index
    echo "Updating package index..."
    sudo apt-get update

    # Install prerequisites
    echo "Installing prerequisites..."
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    # Add Docker's official GPG key
    echo "Adding Docker GPG key..."
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/$DISTRO/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    # Set up repository
    echo "Setting up Docker repository..."
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$DISTRO \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Install Docker Engine
    echo "Installing Docker Engine..."
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
}

# Function to install Docker on Fedora
install_docker_fedora() {
    echo "Installing Docker on Fedora..."

    # Install prerequisites
    echo "Installing prerequisites..."
    sudo dnf -y install dnf-plugins-core

    # Add Docker repository
    echo "Adding Docker repository..."
    sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

    # Install Docker Engine
    echo "Installing Docker Engine..."
    sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
}

# Function to install Docker on Arch Linux
install_docker_arch() {
    echo "Installing Docker on Arch Linux..."

    # Install Docker
    sudo pacman -Sy --noconfirm docker docker-compose
}

# Install based on distribution
echo "[2/4] Installing Docker for your distribution..."
echo

case $DISTRO in
    ubuntu|debian)
        install_docker_debian
        ;;
    fedora)
        install_docker_fedora
        ;;
    arch|manjaro)
        install_docker_arch
        ;;
    *)
        echo -e "${RED}ERROR: Unsupported distribution: $DISTRO${NC}"
        echo
        echo "Please install Docker manually from:"
        echo "https://docs.docker.com/engine/install/"
        exit 1
        ;;
esac

echo
echo -e "${GREEN}[✓] Docker installed successfully${NC}"
echo

echo "[3/4] Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

echo
echo -e "${GREEN}[✓] Docker service started${NC}"
echo

echo "[4/4] Setting up user permissions..."
echo

# Add user to docker group
if ! groups | grep -q docker; then
    sudo usermod -aG docker $USER
    echo -e "${GREEN}[✓] Added $USER to docker group${NC}"
    echo
    echo -e "${YELLOW}IMPORTANT: You need to log out and log back in${NC}"
    echo "for group changes to take effect."
    NEED_RELOGIN=true
else
    echo -e "${GREEN}[✓] User already in docker group${NC}"
    NEED_RELOGIN=false
fi

echo
echo "========================================"
echo "Docker Installation Complete!"
echo "========================================"
echo
echo -e "${GREEN}NEXT STEPS:${NC}"
echo

if [ "$NEED_RELOGIN" = true ]; then
    echo "1. ${YELLOW}LOG OUT AND LOG BACK IN${NC}"
    echo "   This is required for docker group permissions"
    echo
    echo "2. ${YELLOW}VERIFY DOCKER${NC}"
    echo "   Run: docker --version"
    echo "   Run: docker ps"
    echo
    echo "3. ${YELLOW}START ANCESTREE${NC}"
    echo "   - Run: ./scripts/start_ancestree.sh"
    echo "   - Or: python3 scripts/launcher.py"
else
    echo "1. ${YELLOW}VERIFY DOCKER${NC}"
    if docker ps &> /dev/null; then
        echo -e "   ${GREEN}[✓] Docker is running${NC}"
    else
        echo "   Run: docker --version"
        echo "   Run: docker ps"
    fi
    echo
    echo "2. ${YELLOW}START ANCESTREE${NC}"
    echo "   - Run: ./scripts/start_ancestree.sh"
    echo "   - Or: python3 scripts/launcher.py"

    echo
    read -p "Would you like to start AncesTree now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$(dirname "$0")/.."
        python3 scripts/launcher.py
    fi
fi

echo
echo "For help, see: docs/USER_GUIDE.md"
echo
