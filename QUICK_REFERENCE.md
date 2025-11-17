# Ancestree - Quick Reference Guide

**One-page reference for common tasks**

---

## 🚀 For End Users

### Installation (One Command)

```bash
# Windows (as Administrator)
scripts\install_windows.bat

# macOS
./scripts/install_macos.sh

# Linux
./scripts/install_linux.sh
```

### Starting Ancestree

```bash
# Mac
Double-click: scripts/Start Ancestree.command

# Windows
Double-click: scripts/Start Ancestree.bat

# Linux
./scripts/start_ancestree.sh
```

### Stopping Ancestree

```bash
./scripts/stop_ancestree.sh
```

Or in Docker Desktop: Stop the containers

---

## 👨‍💻 For Developers

### Quick Start Development

```bash
# Start with Docker
docker-compose up -d

# Or run manually
# Terminal 1 - Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

### Testing

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test
```

---

## 🏗️ Building Executables

### Option 1: GitHub Actions (Recommended)

```bash
# Create and push a release tag
git tag v1.0.0
git push origin v1.0.0
```

Builds all platforms automatically. Download from GitHub Releases.

### Option 2: Build Locally

```bash
# Windows (on Windows)
scripts\build_windows.bat

# macOS (on Mac)
./scripts/build_macos.sh

# Linux (on Linux)
./scripts/build_linux.sh
```

---

## 📚 Documentation

| Need | Document |
|------|----------|
| **Using the app** | `docs/FOR_USERS.md` |
| **Development** | `docs/FOR_DEVELOPERS.md` |
| **Installing** | `docs/INSTALLATION_GUIDE.md` |
| **Building executables** | `docs/BUILD_INSTRUCTIONS.md` |
| **GitHub Actions** | `.github/README.md` |

---

## 🐳 Docker Commands

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build

# Reset everything
docker-compose down -v
rm backend/ancestree.db
docker-compose up -d --build
```

---

## 🔧 Common Tasks

### Update Database Name References

Already done - all references changed from `family_tree` to `ancestree`

### Add New Python Dependency

```bash
# Backend
cd backend
source venv/bin/activate
pip install package-name
pip freeze > requirements.txt
```

### Add New Frontend Dependency

```bash
# Frontend
cd frontend
npm install package-name
```

### Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Add to `backend/.env`:
```
SECRET_KEY=<generated-key>
```

---

## 🌐 URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | React app |
| **Backend API** | http://localhost:8000 | FastAPI |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **API Docs (Alt)** | http://localhost:8000/redoc | ReDoc |

---

## 📁 Project Structure

```
ancestree/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── scripts/           # Launchers, installers, builders
├── docs/              # All documentation
├── .github/           # GitHub Actions workflows
├── assets/            # Icons and resources
├── docker-compose.yml # Docker orchestration
└── ancestree.spec     # PyInstaller config
```

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Find and kill process
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
kill -9 <PID>
```

### Docker Not Running

```bash
# Mac
open -a Docker

# Check status
docker ps
```

### Build Fails

```bash
# Clean and rebuild
rm -rf build dist *.app *.pkg *.exe *.AppImage
# Run build script again
```

### Reset Database

```bash
# Docker
docker-compose down -v

# Manual
rm backend/ancestree.db
```

---

## 🔗 Useful Links

- **Docker Desktop**: https://www.docker.com/products/docker-desktop
- **Python**: https://www.python.org
- **Node.js**: https://nodejs.org
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev

---

## 💡 Tips

1. **Always activate virtual environment** before working on backend
2. **Use Docker** for simplest deployment
3. **Use GitHub Actions** to build for all platforms
4. **Check logs** when something doesn't work: `docker-compose logs -f`
5. **Read docs/FOR_DEVELOPERS.md** for comprehensive guide

---

## 📞 Getting Help

1. Check documentation in `docs/` directory
2. Review troubleshooting sections
3. Check GitHub Issues (if repository is on GitHub)
4. Review error logs and stack traces

---

**Quick tip**: Keep this file bookmarked for fast reference!
