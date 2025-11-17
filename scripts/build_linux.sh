#!/bin/bash
# Build script for Linux AppImage
# Run this on a Linux machine to create Ancestree-x86_64.AppImage

set -e

echo "========================================"
echo "Building Ancestree for Linux"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.9+"
    exit 1
fi

echo "[1/8] Installing build dependencies..."
pip3 install -r build_requirements.txt

echo
echo "[2/8] Installing AppImage tools..."
# Download appimagetool if not present
if [ ! -f "appimagetool-x86_64.AppImage" ]; then
    echo "Downloading appimagetool..."
    wget -q https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x appimagetool-x86_64.AppImage
fi

echo
echo "[3/8] Cleaning previous builds..."
rm -rf build dist AppDir Ancestree-x86_64.AppImage

echo
echo "[4/8] Building executable with PyInstaller..."
pyinstaller --clean --noconfirm ancestree-linux.spec 2>/dev/null || \
pyinstaller --clean --noconfirm --onefile --windowed --name Ancestree launcher.py

echo
echo "[5/8] Creating AppImage directory structure..."
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps

# Copy executable
if [ -f "dist/Ancestree" ]; then
    cp dist/Ancestree AppDir/usr/bin/ancestree
    chmod +x AppDir/usr/bin/ancestree
else
    echo "❌ Error: Executable not found"
    exit 1
fi

# Copy documentation
cp USER_GUIDE.md TECHNICAL_GUIDE.md QUICK_START.md START_HERE.md AppDir/usr/ 2>/dev/null || true
cp docker-compose.yml AppDir/usr/ 2>/dev/null || true

echo
echo "[6/8] Creating desktop entry..."
cat > AppDir/ancestree.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Ancestree
Comment=Build and explore your family tree
Exec=ancestree
Icon=ancestree
Categories=Utility;
Terminal=false
EOF

# Create a simple icon (text-based for now)
cat > AppDir/usr/share/icons/hicolor/256x256/apps/ancestree.svg << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
  <rect width="256" height="256" fill="#2c3e50"/>
  <text x="128" y="140" font-family="Arial" font-size="120" fill="white" text-anchor="middle">🌳</text>
</svg>
EOF

# Create AppRun script
cat > AppDir/AppRun << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
cd "${HERE}/usr"
exec "${HERE}/usr/bin/ancestree" "$@"
EOF

chmod +x AppDir/AppRun

echo
echo "[7/8] Building AppImage..."
./appimagetool-x86_64.AppImage AppDir Ancestree-x86_64.AppImage

if [ -f "Ancestree-x86_64.AppImage" ]; then
    chmod +x Ancestree-x86_64.AppImage
    echo "✅ AppImage created successfully"
else
    echo "❌ Error: AppImage creation failed"
    exit 1
fi

echo
echo "[8/8] Cleaning up temporary files..."
rm -rf AppDir

echo
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo
echo "AppImage: Ancestree-x86_64.AppImage"
echo "Size: $(du -h Ancestree-x86_64.AppImage | cut -f1)"
echo
echo "Distribution:"
echo "  - Give users Ancestree-x86_64.AppImage"
echo "  - Make it executable: chmod +x Ancestree-x86_64.AppImage"
echo "  - Run with: ./Ancestree-x86_64.AppImage"
echo "  - Users will need Docker installed"
echo
echo "Note: AppImage works on most Linux distributions"
echo
