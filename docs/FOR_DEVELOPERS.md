# 🔧 AncesTree - Developer Guide

**Complete technical documentation for developers**

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture](#architecture)
3. [Development Setup](#development-setup)
4. [Building Executables](#building-executables)
5. [Docker Deployment](#docker-deployment)
6. [API Documentation](#api-documentation)
7. [Database](#database)
8. [Troubleshooting](#troubleshooting)
9. [Production Deployment](#production-deployment)
10. [Contributing](#contributing)

---

## 🚀 Quick Start

### Method 1: Docker (Recommended)

```bash
# Start everything
docker-compose up -d

# Access
open http://localhost:3000  # Mac
# Or http://localhost:3000 in browser
```

### Method 2: Manual Development

```bash
# Terminal 1: Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with SECRET_KEY
python run.py

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

---

## 🏗️ Architecture

### Stack

**Backend:**
- FastAPI 0.104+ (Python web framework)
- SQLAlchemy 2.0+ (ORM)
- SQLite (default) / PostgreSQL (production)
- JWT authentication (python-jose)
- BeautifulSoup4 & Selenium (scraping)
- OpenAI & Anthropic APIs (AI features)

**Frontend:**
- React 18
- Vite (build tool)
- D3.js (tree visualization)
- Zustand (state management)
- Axios (HTTP client)

**Infrastructure:**
- Docker & Docker Compose
- Nginx (production)
- Gunicorn + Uvicorn (production ASGI)

### Project Structure

```
ancestree/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── database.py          # DB config
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # Business logic
│   │   └── utils/               # Helpers
│   ├── requirements.txt
│   ├── run.py
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── stores/              # Zustand stores
│   │   ├── services/            # API client
│   │   └── styles/              # CSS
│   ├── package.json
│   └── vite.config.js
│
├── scripts/                     # Launchers & installers
└── docs/                        # Documentation
```

---

## 💻 Development Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Docker Desktop (for Docker method)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Add to .env: SECRET_KEY=<generated-key>

# Run development server
python run.py
# Or: uvicorn app.main:app --reload --port 8000
```

Backend runs on: http://localhost:8000
API docs: http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on: http://localhost:3000

---

## 🏗️ Building Executables

### Windows (.exe)

```batch
# Must run on Windows
scripts\build_windows.bat

# Output: AncesTree.exe
```

### macOS (.app and .pkg)

```bash
# Must run on macOS
./scripts/build_macos.sh

# Output: AncesTree.app, AncesTree.pkg
```

### Linux (AppImage)

```bash
# Must run on Linux
./scripts/build_linux.sh

# Output: AncesTree-x86_64.AppImage
```

### Requirements

- Python 3.9+
- PyInstaller: `pip install -r build_requirements.txt`
- Must build on target platform

---

## 🐳 Docker Deployment

### Development

```bash
# Start
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

### Production

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/ancestree
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=ancestree
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 🔌 API Documentation

### Interactive Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

**Authentication:**
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Get JWT token
- `GET /api/auth/me` - Current user

**Family Members:**
- `GET /api/family-members` - List all
- `POST /api/family-members` - Create
- `GET /api/family-members/{id}` - Get one
- `PUT /api/family-members/{id}` - Update
- `DELETE /api/family-members/{id}` - Delete

**Documents:**
- `POST /api/documents` - Upload
- `GET /api/documents?member_id={id}` - List
- `DELETE /api/documents/{id}` - Delete

**Search:**
- `POST /api/search/genealogy` - Search records

### Authentication

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -d "username=test&password=test123"

# Use token
TOKEN="your-token"
curl http://localhost:8000/api/family-members \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🗄️ Database

### SQLite (Default)

```bash
# Database file
backend/ancestree.db

# View with sqlite3
sqlite3 backend/ancestree.db
.tables
.schema users
SELECT * FROM users;
```

### PostgreSQL (Production)

```bash
# Install PostgreSQL
# Mac: brew install postgresql
# Ubuntu: apt-get install postgresql

# Create database
createdb ancestree

# Update .env
DATABASE_URL=postgresql://user:password@localhost:5432/ancestree

# Tables created automatically on start
```

### Reset Database

```bash
# SQLite
rm backend/ancestree.db
# Restart backend

# Docker
docker-compose down -v
docker-compose up
```

---

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 in use:**
```bash
lsof -i :8000
kill -9 <PID>
```

**Import errors:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues

**Port 3000 in use:**
```bash
lsof -i :3000
kill -9 <PID>
```

**Module not found:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### Docker Issues

**Cannot connect to daemon:**
```bash
# Start Docker Desktop
open -a Docker  # Mac
```

**Port conflicts:**
```yaml
# Edit docker-compose.yml
ports:
  - "8001:8000"  # Use different port
```

---

## 🚀 Production Deployment

### Backend

```bash
# Install Gunicorn
pip install gunicorn

# Run production server
gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Frontend

```bash
# Build
npm run build

# Serve dist/ with Nginx
cp -r dist/* /var/www/ancestree/
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /var/www/ancestree;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
}
```

---

## 📝 Environment Variables

**Required:**
```env
DATABASE_URL=sqlite:///./ancestree.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Optional:**
```env
# AI Features
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Genealogy APIs
ANCESTRY_API_KEY=...
FAMILYSEARCH_USERNAME=...
FAMILYSEARCH_PASSWORD=...
```

---

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test

# Linting
cd backend
black app/
pylint app/

cd frontend
npm run lint
```

---

## 🤝 Contributing

### Development Workflow

```bash
# Fork repository
git clone https://github.com/yourusername/ancestree
cd ancestree

# Create branch
git checkout -b feature/your-feature

# Make changes
# ...

# Test
pytest
npm test

# Commit
git commit -m "Add feature"
git push origin feature/your-feature

# Create pull request
```

### Code Style

- Backend: PEP 8, use Black formatter
- Frontend: ESLint config
- Write tests for new features
- Update documentation

---

## 📚 Additional Resources

- **FastAPI**: https://fastapi.tiangolo.com
- **React**: https://react.dev
- **D3.js**: https://d3js.org
- **Docker**: https://docs.docker.com

---

## 🔒 Security

### Best Practices

- Change SECRET_KEY in production
- Use HTTPS
- Enable CORS only for your domain
- Use PostgreSQL in production
- Regular dependency updates
- Input validation (handled by Pydantic)
- Rate limiting (implement if needed)

### Database Backups

```bash
# SQLite
cp backend/ancestree.db backup/ancestree_$(date +%Y%m%d).db

# PostgreSQL
pg_dump ancestree > backup/ancestree_$(date +%Y%m%d).sql
```

---

## 📊 Performance

### Optimization

- Use PostgreSQL for production
- Enable caching (Redis)
- Optimize database queries
- Compress frontend assets
- Use CDN for static files
- Implement pagination

---

## 🎯 Release Checklist

- [ ] All tests passing
- [ ] Version numbers updated
- [ ] CHANGELOG updated
- [ ] Documentation updated
- [ ] Build executables
- [ ] Test on clean machines
- [ ] Create GitHub release
- [ ] Upload executables

---

**Happy Developing!** 🚀
