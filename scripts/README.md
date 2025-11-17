# 📜 Scripts Directory

This directory contains all executable scripts for AncesTree.

---

## 🎯 Automated Installers (NEW!)

**One-command installation - Easiest way to get started!**

| Script | Platform | What It Does |
|--------|----------|--------------|
| `install_windows.bat` | Windows | Installs Docker Desktop + sets up AncesTree |
| `install_macos.sh` | macOS | Installs Docker Desktop + sets up AncesTree |
| `install_linux.sh` | Linux | Installs Docker Engine + sets up AncesTree |

### How to Use Installers

**Windows:**
```batch
# Right-click and "Run as Administrator"
scripts\install_windows.bat
```

**Mac:**
```bash
./scripts/install_macos.sh
```

**Linux:**
```bash
./scripts/install_linux.sh
```

**See [docs/INSTALLATION_GUIDE.md](../docs/INSTALLATION_GUIDE.md) for complete instructions.**

---

## 🚀 Launcher Scripts

**For End Users (after Docker is installed):**

| Script | Platform | Description |
|--------|----------|-------------|
| `Start AncesTree.command` | macOS | Double-click to start on Mac |
| `Start AncesTree.bat` | Windows | Double-click to start on Windows |
| `launcher.py` | All | GUI launcher (cross-platform) |
| `start_ancestree.sh` | Linux/Mac | Shell script to start with Docker |
| `stop_ancestree.sh` | Linux/Mac | Shell script to stop services |

### How to Use

**Mac Users:**
```bash
# From project root
./scripts/"Start AncesTree.command"

# Or just double-click it in Finder
```

**Windows Users:**
```batch
# From project root
scripts\"Start AncesTree.bat"

# Or just double-click it in Explorer
```

**Linux Users:**
```bash
# From project root
./scripts/start_ancestree.sh
```

**Any Platform (with Python):**
```bash
# From project root
python3 scripts/launcher.py
```

---

## 🏗️ Build Scripts

**For Developers Creating Executables:**

| Script | Platform | Output |
|--------|----------|--------|
| `build_windows.bat` | Windows | `AncesTree.exe` |
| `build_macos.sh` | macOS | `AncesTree.app` + `AncesTree.pkg` |
| `build_linux.sh` | Linux | `AncesTree-x86_64.AppImage` |

### How to Build

**Windows Executable:**
```batch
# Must run on Windows
cd scripts
build_windows.bat
```

**macOS Application:**
```bash
# Must run on macOS
cd scripts
./build_macos.sh
```

**Linux AppImage:**
```bash
# Must run on Linux
cd scripts
./build_linux.sh
```

See `docs/BUILD_INSTRUCTIONS.md` for complete build documentation.

---

## 📝 Script Details

### Launcher Scripts

**`launcher.py`**
- Python/tkinter GUI launcher
- Supports Docker and Manual modes
- Auto-opens browser
- Visual feedback and status
- Cross-platform

**`Start AncesTree.command` (Mac)**
- Wrapper for launcher.py
- Double-click friendly
- Checks for Python installation

**`Start AncesTree.bat` (Windows)**
- Wrapper for launcher.py
- Double-click friendly
- Checks for Python installation

**`start_ancestree.sh` (Linux/Mac)**
- Docker-based startup
- Command-line interface
- Checks Docker installation
- Auto-opens browser

**`stop_ancestree.sh` (Linux/Mac)**
- Stops Docker services
- Clean shutdown

### Build Scripts

**`build_windows.bat`**
- Builds Windows .exe
- Uses PyInstaller
- ~25-35 MB output
- Requires Windows OS

**`build_macos.sh`**
- Builds macOS .app bundle
- Creates .pkg installer
- Optional code signing
- ~30-40 MB output
- Requires macOS

**`build_linux.sh`**
- Builds AppImage
- Universal Linux executable
- ~35-45 MB output
- Requires Linux OS

---

## 🔧 Requirements

### To Run Launchers

- **Docker Desktop** (required)
- **Python 3.9+** (for Python launcher)

### To Build Executables

- **Python 3.9+**
- **PyInstaller** (`pip install -r ../build_requirements.txt`)
- Platform-specific: Must build on target OS

---

## 📖 Documentation

- **User Guide**: `../docs/USER_GUIDE.md`
- **Technical Guide**: `../docs/TECHNICAL_GUIDE.md`
- **Build Instructions**: `../docs/BUILD_INSTRUCTIONS.md`
- **Quick Start**: `../docs/QUICK_START.md`

---

## 🆘 Troubleshooting

**"Python not found"**
- Install Python 3.9+ from https://www.python.org
- Make sure it's in your PATH

**"Docker not found"**
- Install Docker Desktop from https://www.docker.com/products/docker-desktop
- Make sure Docker is running

**"Permission denied"**
```bash
# Make scripts executable
chmod +x *.sh *.command launcher.py
```

**"Script won't run"**
- Make sure you're in the project root directory
- Check that Docker Desktop is running
- See troubleshooting in `../docs/TECHNICAL_GUIDE.md`

---

## 💡 Tips

- **Double-click launchers** work from any location
- **Shell scripts** should be run from project root
- **Build scripts** create executables in project root
- **Always test** executables on clean machines

---

**Need Help?** Check `docs/` directory for comprehensive guides.
