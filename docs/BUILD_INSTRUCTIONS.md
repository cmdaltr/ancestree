# 🏗️ Building Executable Packages

This guide explains how to build platform-specific executable packages for Ancestree.

---

## ⚡ Quick Start (Recommended)

### GitHub Actions - Automatic Cross-Platform Builds

**The easiest way to build for all platforms is using GitHub Actions** - no need for multiple operating systems!

```bash
# Create a release tag
git tag v1.0.0
git push origin v1.0.0
```

GitHub will automatically:
- ✅ Build Windows .exe
- ✅ Build macOS .app/.dmg
- ✅ Build Linux AppImage
- ✅ Create a GitHub Release with all executables

See [`.github/README.md`](../.github/README.md) for details.

---

## 🔨 Manual Building (Alternative)

If you prefer to build manually or need to test locally:

---

## 📦 What Gets Built

| Platform | Output | Description |
|----------|--------|-------------|
| **Windows** | `Ancestree.exe` | Standalone executable |
| **macOS** | `Ancestree.app` | macOS application bundle |
| **macOS** | `Ancestree.pkg` | macOS installer package |
| **Linux** | `Ancestree-x86_64.AppImage` | Universal Linux executable |

---

## 🔧 Prerequisites

### All Platforms
- Python 3.9 or higher
- Git (to clone the repository)

### Platform-Specific

**Windows:**
- Windows 7 or higher
- Administrator access (for installing packages)

**macOS:**
- macOS 10.13 (High Sierra) or higher
- Xcode Command Line Tools: `xcode-select --install`
- Optional: Apple Developer account (for code signing)

**Linux:**
- Any modern Linux distribution (Ubuntu 20.04+, Fedora 35+, etc.)
- `wget` or `curl` installed

---

## 🚀 Building Executables

### Windows Executable (.exe)

**Run on a Windows machine:**

```batch
# Method 1: Using the build script
build_windows.bat

# Method 2: Manual build
pip install -r build_requirements.txt
pyinstaller --clean --noconfirm ancestree.spec
copy dist\Ancestree.exe .
```

**Output:**
- `Ancestree.exe` - Standalone executable (~20-30 MB)

**Testing:**
```batch
# Double-click Ancestree.exe or run:
Ancestree.exe
```

---

### macOS Application (.app and .pkg)

**Run on a Mac:**

```bash
# Method 1: Using the build script
./build_macos.sh

# Method 2: Manual build
pip3 install -r build_requirements.txt
pyinstaller --clean --noconfirm ancestree.spec
cp -R dist/Ancestree.app .
```

**Output:**
- `Ancestree.app` - Application bundle (drag to Applications folder)
- `Ancestree.pkg` - Installer package (double-click to install)

**Code Signing (Optional but Recommended):**
```bash
# Set your Developer ID
export CODESIGN_IDENTITY="Developer ID Application: Your Name (TEAM_ID)"
./build_macos.sh
```

**Testing:**
```bash
# Open the app
open Ancestree.app

# Or double-click in Finder
```

**Note:** Users may see "unverified developer" warning. Tell them to:
1. Right-click the app
2. Select "Open"
3. Click "Open" in the dialog

---

### Linux AppImage

**Run on a Linux machine:**

```bash
# Method 1: Using the build script
./build_linux.sh

# Method 2: Manual build
pip3 install -r build_requirements.txt
pyinstaller --clean --noconfirm --onefile --windowed --name Ancestree launcher.py
# Then follow AppImage creation steps in build_linux.sh
```

**Output:**
- `Ancestree-x86_64.AppImage` - Universal Linux executable (~30-40 MB)

**Testing:**
```bash
chmod +x Ancestree-x86_64.AppImage
./Ancestree-x86_64.AppImage
```

---

## 🎨 Custom Icon (Optional)

To add a custom icon to the executables:

### Create Icon Files

1. **Design a 512x512 PNG icon** (family tree theme)

2. **Convert to platform formats:**

**Windows (.ico):**
```bash
# Using ImageMagick
convert icon.png -define icon:auto-resize=256,128,64,48,32,16 assets/icon.ico
```

**macOS (.icns):**
```bash
# Using iconutil (macOS)
mkdir icon.iconset
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
cp icon.png icon.iconset/icon_512x512@2x.png
iconutil -c icns icon.iconset -o assets/icon.icns
```

**Linux (.png):**
```bash
cp icon.png assets/icon.png
```

### Update Build Configuration

The `ancestree.spec` file is already configured to use icons from `assets/` directory.

---

## 📊 Build Output Sizes

Typical executable sizes:

| Platform | Size | Notes |
|----------|------|-------|
| Windows EXE | 25-35 MB | Includes Python runtime |
| macOS APP | 30-40 MB | Application bundle |
| macOS PKG | 30-40 MB | Compressed installer |
| Linux AppImage | 35-45 MB | Includes dependencies |

**Note:** Sizes may vary based on Python version and included dependencies.

---

## 🐛 Troubleshooting

### Windows

**Problem: "Python not found"**
- Install Python from https://www.python.org
- Make sure to check "Add Python to PATH"

**Problem: "PyInstaller failed"**
- Run as Administrator
- Disable antivirus temporarily
- Check Windows Defender exclusions

**Problem: Executable won't run**
- Check for antivirus blocks
- Try running from command prompt to see errors

### macOS

**Problem: "Command not found: pyinstaller"**
```bash
pip3 install --upgrade pip
pip3 install -r build_requirements.txt
```

**Problem: "Developer cannot be verified"**
- This is normal for unsigned apps
- Right-click → Open → Open to bypass
- Or: System Preferences → Security & Privacy → Allow

**Problem: Code signing fails**
- Make sure you have a Developer ID certificate
- Check: `security find-identity -v -p codesigning`

### Linux

**Problem: "AppImage won't run"**
```bash
# Make sure it's executable
chmod +x AncesTree-x86_64.AppImage

# Install FUSE if needed
sudo apt install fuse libfuse2  # Debian/Ubuntu
sudo dnf install fuse fuse-libs  # Fedora
```

**Problem: "No such file or directory: appimagetool"**
- The script will download it automatically
- Or download manually from: https://github.com/AppImage/AppImageKit/releases

**Problem: Build fails with Python errors**
```bash
# Install Python 3.9+
sudo apt install python3.9 python3.9-dev python3-pip  # Ubuntu
sudo dnf install python39 python39-devel  # Fedora

# Use specific Python version
python3.9 -m pip install -r build_requirements.txt
python3.9 -m PyInstaller ancestree.spec
```

---

## 📦 Distribution

### For End Users

**Include in your release:**
1. The executable (`.exe`, `.app`, `.pkg`, or `.AppImage`)
2. `USER_GUIDE.md` - User instructions
3. `START_HERE.md` - Quick start guide
4. A README explaining:
   - Docker Desktop is required
   - Installation instructions
   - First-time usage

### Recommended Distribution Methods

**Windows:**
- Upload `Ancestree.exe` to GitHub Releases
- Or create installer with [Inno Setup](https://jrsoftware.org/isinfo.php)
- Or create installer with [NSIS](https://nsis.sourceforge.io/)

**macOS:**
- Distribute `Ancestree.pkg` for easy installation
- Or provide `Ancestree.app` with instructions to drag to Applications
- Consider notarization for better user experience

**Linux:**
- Distribute `Ancestree-x86_64.AppImage`
- Works on most distributions without installation
- Users just need to make it executable

### GitHub Release Example

```bash
# Tag the release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Upload to GitHub Releases:
# - Ancestree.exe (Windows)
# - Ancestree.pkg (macOS installer)
# - Ancestree.app.zip (macOS app bundle, zipped)
# - Ancestree-x86_64.AppImage (Linux)
# - Source code (automatic)
# - USER_GUIDE.md
# - START_HERE.md
```

---

## 🔒 Security Notes

### Code Signing

**Why sign your executables?**
- Users won't see scary warnings
- Establishes trust
- Required for macOS Gatekeeper
- Recommended for Windows SmartScreen

**Windows Code Signing:**
- Requires a code signing certificate (~$100-300/year)
- Providers: DigiCert, Sectigo, GlobalSign
- Use `signtool` to sign the executable

**macOS Code Signing:**
- Requires Apple Developer account ($99/year)
- Use `codesign` command
- Consider notarization for Catalina+

**Linux:**
- Generally not required
- AppImages can be signed with GPG

### Antivirus False Positives

PyInstaller executables sometimes trigger antivirus warnings:

**Solutions:**
1. **Sign your executable** (best solution)
2. **Submit to antivirus vendors** for whitelisting
3. **Build on clean VM** (reduces detection)
4. **Use specific PyInstaller version** (some versions trigger less)

---

## 🚀 Automated Builds (CI/CD)

### GitHub Actions Example

Create `.github/workflows/build.yml`:

```yaml
name: Build Executables

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r build_requirements.txt
      - run: pyinstaller --clean --noconfirm ancestree.spec
      - uses: actions/upload-artifact@v3
        with:
          name: Ancestree-Windows
          path: dist/Ancestree.exe

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r build_requirements.txt
      - run: pyinstaller --clean --noconfirm ancestree.spec
      - run: zip -r Ancestree.app.zip dist/Ancestree.app
      - uses: actions/upload-artifact@v3
        with:
          name: Ancestree-macOS
          path: Ancestree.app.zip

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: sudo apt-get install -y fuse libfuse2
      - run: ./build_linux.sh
      - uses: actions/upload-artifact@v3
        with:
          name: Ancestree-Linux
          path: Ancestree-x86_64.AppImage
```

---

## 📝 Checklist for Distribution

Before distributing your executables:

- [ ] Test on clean machine without Python installed
- [ ] Test with Docker Desktop installed
- [ ] Test without Docker Desktop (should show error)
- [ ] Verify all documentation is included
- [ ] Check executable size is reasonable
- [ ] Test on minimum supported OS version
- [ ] Verify error messages are user-friendly
- [ ] Test auto-browser opening
- [ ] Consider code signing (recommended)
- [ ] Create release notes
- [ ] Update version numbers
- [ ] Test installation process

---

## 🎯 Quick Reference

```bash
# Windows (on Windows machine)
build_windows.bat

# macOS (on Mac)
./build_macos.sh

# Linux (on Linux machine)
./build_linux.sh

# Output files:
# - Ancestree.exe (Windows)
# - Ancestree.app (macOS app)
# - Ancestree.pkg (macOS installer)
# - Ancestree-x86_64.AppImage (Linux)
```

---

## 💡 Tips

1. **Build on target platform** - Always build on the platform you're targeting
2. **Test thoroughly** - Test on clean machines without development tools
3. **Version your builds** - Include version numbers in filenames
4. **Document requirements** - Make sure users know they need Docker Desktop
5. **Provide support** - Include troubleshooting guides with distribution
6. **Keep it simple** - The executable should "just work" for end users
7. **Update regularly** - Keep PyInstaller and dependencies up to date

---

## 📞 Support

For build issues:
- Check PyInstaller documentation: https://pyinstaller.org
- Review error messages carefully
- Test on clean VM/machine
- Check antivirus/firewall settings

For distribution questions:
- See TECHNICAL_GUIDE.md
- Review platform-specific guidelines
- Consider your target audience's technical level

---

**Happy Building! 🏗️**
