# 📦 Installation Guide - Automated Installers

This guide explains how to use the automated installers to set up AncesTree on any platform.

---

## 🎯 What the Installers Do

The automated installers will:

1. ✅ **Check** if Docker is already installed
2. 📥 **Download** Docker Desktop (if needed)
3. 🔧 **Install** Docker Desktop automatically
4. ⚙️ **Configure** Docker for your system
5. 🚀 **Guide you** to start AncesTree

**All completely automatic!** Just run one command.

---

## 🪟 Windows Installation

### One-Click Install

1. **Right-click** `scripts/install_windows.bat`
2. Select **"Run as administrator"** (Important!)
3. Follow the prompts

### What Happens

```batch
# The installer will:
- Check for Docker
- Download Docker Desktop (~500 MB)
- Install Docker Desktop
- Prompt you to restart
```

### After Installation

1. **Restart your computer** (required)
2. **Open Docker Desktop** from Start Menu
3. **Wait** for Docker to start (whale icon in system tray)
4. **Run AncesTree**:
   - Double-click `scripts/Start AncesTree.bat`
   - Or run `python scripts/launcher.py`

### Requirements

- **Windows 10/11** (64-bit)
- **Administrator access**
- **Internet connection** (~500 MB download)
- **8 GB RAM** minimum (16 GB recommended)

### Troubleshooting

**"Not recognized as administrator"**
- Right-click the file → Run as administrator

**"Download failed"**
- Check internet connection
- Download manually: https://www.docker.com/products/docker-desktop

**"Installation failed"**
- Ensure Windows is up to date
- Check that virtualization is enabled in BIOS

---

## 🍎 macOS Installation

### One-Click Install

```bash
# From project root
./scripts/install_macos.sh
```

Or just **double-click** `scripts/install_macos.sh` in Finder.

### What Happens

```bash
# The installer will:
- Detect your Mac type (Intel or Apple Silicon)
- Download correct Docker Desktop (~600 MB)
- Install Docker.app to /Applications
- Guide you through first launch
```

### After Installation

1. **Launch Docker Desktop** from Applications
2. **Accept** terms and conditions
3. **Grant** privileged access (may ask for password)
4. **Wait** for Docker to start (2-3 minutes first time)
5. **Run AncesTree**:
   - Double-click `scripts/Start AncesTree.command`
   - Or run `./scripts/start_ancestree.sh`
   - Or run `python3 scripts/launcher.py`

### Requirements

- **macOS 10.15+** (Catalina or later)
- **Intel or Apple Silicon** (auto-detected)
- **Internet connection** (~600 MB download)
- **8 GB RAM** minimum (16 GB recommended)

### Troubleshooting

**"Permission denied"**
```bash
chmod +x scripts/install_macos.sh
./scripts/install_macos.sh
```

**"Cannot be opened because the developer cannot be verified"**
- Right-click → Open → Open

**"Download failed"**
- Check internet connection
- Download manually: https://www.docker.com/products/docker-desktop

---

## 🐧 Linux Installation

### One-Click Install

```bash
# From project root
./scripts/install_linux.sh
```

### What Happens

```bash
# The installer will:
- Detect your Linux distribution
- Install Docker Engine
- Start Docker service
- Add you to docker group
- Set up auto-start
```

### Supported Distributions

- ✅ **Ubuntu** 20.04+
- ✅ **Debian** 10+
- ✅ **Fedora** 35+
- ✅ **Arch Linux**
- ✅ **Manjaro**

### After Installation

**Important:** Log out and log back in (required for group permissions)

Then run AncesTree:
```bash
./scripts/start_ancestree.sh
# Or
python3 scripts/launcher.py
```

### Requirements

- **Supported Linux distribution**
- **sudo access**
- **Internet connection**
- **4 GB RAM** minimum (8 GB recommended)

### Troubleshooting

**"Permission denied"**
```bash
chmod +x scripts/install_linux.sh
sudo ./scripts/install_linux.sh
```

**"Unsupported distribution"**
- Install Docker manually: https://docs.docker.com/engine/install/

**"Cannot run docker without sudo"**
- Log out and log back in
- Or run: `newgrp docker`

---

## 🚀 Quick Start After Installation

Once Docker is installed and running:

### Option 1: GUI Launcher (Easiest)

```bash
# Windows
python scripts\launcher.py

# Mac/Linux
python3 scripts/launcher.py
```

### Option 2: Double-Click Scripts

- **Windows:** Double-click `scripts/Start AncesTree.bat`
- **Mac:** Double-click `scripts/Start AncesTree.command`
- **Linux:** Run `./scripts/start_ancestree.sh`

### Option 3: Docker Directly

```bash
docker-compose up -d
open http://localhost:3000  # Mac
# Or navigate to http://localhost:3000 in browser
```

---

## 📊 Installation Comparison

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Automated Installer** | ✅ One command<br>✅ No manual steps<br>✅ Handles everything | ⚠️ Large download<br>⚠️ Needs admin | Everyone |
| **Manual Docker Install** | ✅ More control<br>✅ Can use existing Docker | ⚠️ Multiple steps<br>⚠️ More complex | Tech users |
| **Pre-built Executable** | ✅ No Docker needed<br>✅ Single file | ⚠️ Still needs Docker for backend | Not available yet |

---

## 🔍 Verifying Installation

After installation, verify Docker is working:

### Check Docker Version

```bash
# Windows
docker --version

# Mac/Linux
docker --version
```

Expected output:
```
Docker version 24.0.0, build abc1234
```

### Check Docker is Running

```bash
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

If you see this (even if empty), Docker is working!

### Check Docker Compose

```bash
docker-compose --version
```

Expected output:
```
Docker Compose version v2.x.x
```

---

## 🆘 Common Issues

### Windows

**Issue:** "Hyper-V is not enabled"
**Solution:**
1. Open PowerShell as Administrator
2. Run: `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All`
3. Restart computer

**Issue:** "WSL 2 installation is incomplete"
**Solution:**
1. Download WSL 2: https://aka.ms/wsl2kernel
2. Install and restart
3. Re-run Docker Desktop installer

### macOS

**Issue:** "Docker Desktop requires macOS 10.15 or later"
**Solution:** Update macOS or use an older Docker version

**Issue:** "Rosetta 2 is required"
**Solution:** Install Rosetta 2:
```bash
softwareupdate --install-rosetta
```

### Linux

**Issue:** "Cannot connect to Docker daemon"
**Solution:**
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

**Issue:** "Permission denied"
**Solution:**
```bash
sudo usermod -aG docker $USER
# Log out and log back in
```

---

## 📦 Disk Space Requirements

| Platform | Docker Download | Installed Size | Free Space Needed |
|----------|----------------|----------------|-------------------|
| Windows | ~500 MB | ~2 GB | 5 GB recommended |
| macOS | ~600 MB | ~2.5 GB | 6 GB recommended |
| Linux | ~200 MB | ~1.5 GB | 4 GB recommended |

Plus space for:
- AncesTree containers (~500 MB)
- Your family tree data (varies)

---

## 🔒 Security Notes

### What the Installers Do

The installers:
- ✅ Download from official Docker sources only
- ✅ Use HTTPS for all downloads
- ✅ Don't collect any personal data
- ✅ Don't modify system files (except Docker installation)

### Permissions Required

- **Windows:** Administrator (for software installation)
- **macOS:** User password (for /Applications access)
- **Linux:** sudo (for package installation)

### What Gets Installed

- Docker Engine
- Docker Compose
- Docker CLI tools
- Container runtime

**Nothing else!** No bundled software, no adware.

---

## 🎓 Advanced Options

### Custom Docker Installation

If you prefer to install Docker manually:

1. **Download** from https://www.docker.com/products/docker-desktop
2. **Install** following Docker's instructions
3. **Skip** the automated installer
4. **Run** AncesTree directly

### Using Existing Docker

If you already have Docker:

```bash
# Just verify it works
docker --version
docker ps

# Then start AncesTree
./scripts/start_ancestree.sh
```

### Offline Installation

For computers without internet:

1. **Download** Docker installer on another computer
2. **Copy** to target computer via USB
3. **Install** Docker manually
4. **Copy** AncesTree project files
5. **Run** AncesTree

---

## 📞 Getting Help

### Installation Failed?

1. **Check** the error message
2. **Try** manual Docker installation
3. **See** troubleshooting sections above
4. **Read** docs/TECHNICAL_GUIDE.md

### Docker Won't Start?

1. **Restart** your computer
2. **Check** system requirements
3. **Verify** virtualization is enabled
4. **See** Docker troubleshooting: https://docs.docker.com/desktop/troubleshoot/overview/

### Still Stuck?

- Check docs/USER_GUIDE.md
- Check docs/TECHNICAL_GUIDE.md
- Review Docker documentation
- Check system requirements

---

## ✅ Installation Checklist

Before you start:
- [ ] System meets requirements
- [ ] Have administrator/sudo access
- [ ] Have stable internet connection
- [ ] Have sufficient disk space

During installation:
- [ ] Installer ran without errors
- [ ] Docker Desktop installed
- [ ] Computer restarted (if required)
- [ ] Docker Desktop started

After installation:
- [ ] `docker --version` works
- [ ] `docker ps` works
- [ ] Can start AncesTree
- [ ] Browser opens to http://localhost:3000

---

## 🎉 Success!

Once you see the AncesTree login page in your browser, you're all set!

**Next steps:**
1. Read docs/USER_GUIDE.md
2. Create your account
3. Start building your family tree!

---

**Happy Installing! 📦**
