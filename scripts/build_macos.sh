#!/bin/bash
# Build script for macOS application bundle and installer
# Run this on a Mac to create Ancestree.app and Ancestree.pkg

set -e

echo "========================================"
echo "Building Ancestree for macOS"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org"
    exit 1
fi

echo "[1/7] Setting up virtual environment..."
# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

echo "Installing build dependencies..."
pip3 install -r build_requirements.txt

echo
echo "[2/7] Cleaning previous builds..."
rm -rf build dist Ancestree.app Ancestree.pkg

echo
echo "[3/7] Building application with PyInstaller..."
# Ensure we're using pyinstaller from the virtual environment
python3 -m PyInstaller --clean --noconfirm ancestree.spec

echo
echo "[4/7] Copying app bundle to root directory..."
if [ -d "dist/Ancestree.app" ]; then
    cp -R dist/Ancestree.app .
    echo "✅ Application created: Ancestree.app"
else
    echo "❌ Error: Build failed"
    exit 1
fi

echo
echo "[5/7] Code signing (optional)..."
if [ -n "$CODESIGN_IDENTITY" ]; then
    echo "Signing with identity: $CODESIGN_IDENTITY"
    codesign --force --deep --sign "$CODESIGN_IDENTITY" Ancestree.app
else
    echo "⚠️  Skipping code signing (set CODESIGN_IDENTITY to enable)"
    echo "   Note: Users may see 'unverified developer' warning"
fi

echo
echo "[6/7] Creating installer package (.pkg)..."

# Create a temporary directory for package building
mkdir -p package_build/Applications
cp -R Ancestree.app package_build/Applications/

# Build the package
pkgbuild --root package_build \
         --identifier com.ancestree.launcher \
         --version 1.0.0 \
         --install-location /Applications \
         --scripts package_scripts \
         Ancestree-component.pkg 2>/dev/null || \
pkgbuild --root package_build \
         --identifier com.ancestree.launcher \
         --version 1.0.0 \
         --install-location /Applications \
         Ancestree-component.pkg

# Create product archive
productbuild --synthesize --package Ancestree-component.pkg distribution.xml 2>/dev/null || true

# Build final installer
productbuild --distribution distribution.xml \
             --package-path . \
             --resources . \
             Ancestree.pkg 2>/dev/null || \
cp Ancestree-component.pkg Ancestree.pkg

echo "✅ Installer created: Ancestree.pkg"

echo
echo "[7/7] Cleaning up temporary files..."
rm -rf package_build Ancestree-component.pkg distribution.xml

echo
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo
echo "Application: Ancestree.app"
echo "Installer:   Ancestree.pkg"
echo
ls -lh Ancestree.app Ancestree.pkg 2>/dev/null || ls -lh Ancestree.app
echo
echo "Distribution:"
echo "  - Give users Ancestree.pkg for easy installation"
echo "  - Or they can drag Ancestree.app to Applications folder"
echo "  - Users will need Docker Desktop installed"
echo
echo "Note: Users may see security warning on first launch."
echo "      Tell them to: Right-click → Open → Open"
echo
