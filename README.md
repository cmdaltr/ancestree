<div align="center">
  <img src="ancestree.png" alt="Ancestree Logo" width="200"/>

  # Ancestree

  **A simple, beautiful family tree application for everyone**

  Build and explore your family history with an easy-to-use interface. Perfect for beginners and tech-savvy genealogists alike.
</div>

---

## 🚀 Quick Start (For Everyone!)

### 🎯 Super Easy - Automated Installation! (Recommended)

**One command installs everything** (including Docker):

```bash
# Windows (Run as Administrator)
scripts\install_windows.bat

# Mac
./scripts/install_macos.sh

# Linux
./scripts/install_linux.sh
```

**That's it!** The installer will:
- ✅ Check if Docker is installed
- ✅ Download and install Docker if needed
- ✅ Set everything up automatically
- ✅ Guide you to start Ancestree

**See [INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) for detailed instructions.**

---

### Alternative 1: Pre-Built Executables

**Build executables for all platforms automatically with GitHub Actions!**

```bash
# Create and push a release tag
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions will build executables for Windows, macOS, and Linux automatically. Download from the Releases page.

**Or build locally**:
- **Windows**: Run `scripts/build_windows.bat` to create `Ancestree.exe`
- **Mac**: Run `./scripts/build_macos.sh` to create `Ancestree.app` and `Ancestree.pkg`
- **Linux**: Run `./scripts/build_linux.sh` to create `Ancestree-x86_64.AppImage`

See [BUILD_INSTRUCTIONS.md](docs/BUILD_INSTRUCTIONS.md) for details.

**Note:** Even with executables, Docker Desktop is still required (use automated installer above)

---

### Alternative 2: Use the Launcher Scripts

If you have the source code:

1. **Install Docker Desktop** (one-time setup):
   - Download from: https://www.docker.com/products/docker-desktop
   - Install and start Docker Desktop

2. **Start Ancestree**:
   - **Mac**: Double-click `scripts/Start Ancestree.command`
   - **Windows**: Double-click `scripts/Start Ancestree.bat`
   - **Linux**: Run `./scripts/start_ancestree.sh`

3. **That's it!** The app opens in your browser automatically 🎉

📖 **First time using it?** Read [FOR_USERS.md](docs/FOR_USERS.md) - simple guide for everyone!

👨‍💻 **Technical user?** See [FOR_DEVELOPERS.md](docs/FOR_DEVELOPERS.md) for complete technical docs.

---

## ✨ Features

- 🌲 **Interactive Family Tree Visualization**: D3.js-powered tree view with zoom and pan
- 🤖 **AI-Powered Search**: Intelligent genealogy record search across multiple sources
- 🌍 **Multi-Source Search**: Search Ancestry.com, FamilySearch, Findmypast, and MyHeritage
- 📸 **Document Management**: Upload and manage photos and documents for family members
- 👤 **Adjustable Side Panel**: View and edit member details with resizable panel
- 🔐 **User Authentication**: Secure JWT-based authentication - your data is private
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices
- 🐳 **Easy Docker Setup**: One-command deployment with Docker
- 🖱️ **Graphical Launcher**: Simple GUI launcher for non-technical users
- 🤖 **Automated Builds**: GitHub Actions builds executables for all platforms automatically

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Default database (easily configurable to PostgreSQL)
- **BeautifulSoup4 & Selenium**: Web scraping capabilities
- **OpenAI & Anthropic**: AI-powered search and analysis
- **Python-Jose**: JWT authentication

### Frontend
- **React 18**: Modern UI library
- **Vite**: Fast build tool and dev server
- **D3.js**: Interactive tree visualization
- **Zustand**: State management
- **Axios**: HTTP client
- **React Router**: Navigation

## Project Structure

```
ancestree/
├── backend/
│   ├── app/
│   │   ├── models.py              # Database models
│   │   ├── schemas.py             # Pydantic schemas
│   │   ├── database.py            # Database configuration
│   │   ├── main.py                # FastAPI application
│   │   ├── routes/                # API routes
│   │   │   ├── auth.py            # Authentication
│   │   │   ├── family_members.py  # Family member CRUD
│   │   │   ├── documents.py       # Document uploads
│   │   │   └── search.py          # Genealogy search
│   │   ├── services/              # Business logic
│   │   │   ├── genealogy_scraper.py  # Web scraping
│   │   │   └── ai_search.py       # AI integration
│   │   └── utils/                 # Utilities
│   │       └── auth.py            # Auth helpers
│   ├── uploads/                   # Uploaded files
│   ├── requirements.txt           # Python dependencies
│   └── .env.example              # Environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── components/            # React components
│   │   ├── stores/                # Zustand stores
│   │   ├── services/              # API services
│   │   └── styles/                # CSS files
│   ├── package.json              # Node dependencies
│   └── vite.config.js           # Vite configuration
│
├── scripts/                     # All executable scripts
│   ├── launcher.py              # GUI launcher
│   ├── Start Ancestree.command  # Mac launcher
│   ├── Start Ancestree.bat      # Windows launcher
│   ├── start_ancestree.sh       # Linux/Mac startup
│   ├── stop_ancestree.sh        # Stop script
│   ├── build_windows.bat        # Build Windows .exe
│   ├── build_macos.sh           # Build macOS .app/.pkg
│   └── build_linux.sh           # Build Linux AppImage
│
├── docs/                        # All documentation
│   ├── START_HERE.md            # First-time user guide
│   ├── QUICK_START.md           # Quick start guide
│   ├── USER_GUIDE.md            # Non-technical user guide
│   ├── TECHNICAL_GUIDE.md       # Developer documentation
│   ├── BUILD_INSTRUCTIONS.md    # How to build executables
│   ├── SETUP.md                 # Development setup
│   ├── RELEASE_CHECKLIST.md     # Release process
│   ├── EXECUTABLES_SUMMARY.md   # Distribution guide
│   └── CHANGES_SUMMARY.md       # Project changes log
│
├── assets/                      # Icons and resources
├── docker-compose.yml           # Docker orchestration
├── ancestree.spec               # PyInstaller config
├── build_requirements.txt       # Build dependencies
└── README.md                    # This file
```

---

## 📚 Documentation

**Simple, consolidated documentation** in the `docs/` directory:

- **[FOR_USERS.md](docs/FOR_USERS.md)** - 👥 Complete guide for non-technical users
- **[FOR_DEVELOPERS.md](docs/FOR_DEVELOPERS.md)** - 🔧 Complete guide for developers
- **[INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md)** - 📦 Automated installer details
- **[BUILD_INSTRUCTIONS.md](docs/BUILD_INSTRUCTIONS.md)** - 🏗️ How to build executables
- **[CICD_PIPELINE.md](docs/CICD_PIPELINE.md)** - 🔄 CI/CD automation with GitHub Actions

All scripts are in the `scripts/` directory ([see full list](scripts/README.md))

---

## 🐳 Installation Methods

### Method 1: Docker (Recommended for End Users)

**Easiest way - requires only Docker Desktop**

1. Install Docker Desktop from https://www.docker.com/products/docker-desktop
2. Use the graphical launcher or run:
   ```bash
   docker-compose up -d
   ```
3. Access at http://localhost:3000

**Benefits**: Zero configuration, works everywhere, production-ready

### Method 2: Graphical Launcher (Best for Non-Technical Users)

1. Install Docker Desktop (see above)
2. Double-click the launcher for your platform:
   - Mac: `Start Ancestree.command`
   - Windows: `Start Ancestree.bat`
   - Any: `launcher.py` (requires Python)

**Benefits**: Visual interface, automatic browser opening, status updates

### Method 3: Manual Setup (For Developers)

**Prerequisites:**
- Python 3.9+
- Node.js 18+
- npm or yarn

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd ancestree/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
```

5. Edit `.env` and add your configuration:
```env
DATABASE_URL=sqlite:///./ancestree.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional: Add AI API keys for enhanced search
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Optional: Add genealogy site credentials
ANCESTRY_API_KEY=your-ancestry-api-key
FAMILYSEARCH_USERNAME=your-username
FAMILYSEARCH_PASSWORD=your-password
```

6. Run the backend:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd ancestree/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

**See [FOR_DEVELOPERS.md](docs/FOR_DEVELOPERS.md) for complete development setup**

---

## 🎯 Usage

### For Non-Technical Users

**Read [FOR_USERS.md](docs/FOR_USERS.md)** - complete guide with step-by-step instructions!

### Getting Started (Quick Version)

1. **Create Account**: Click "Register" on first visit
2. **Login**: Enter your username and password
3. **Add Members**: Click "+ Add Member" button to add people
4. **Build Tree**: Connect family members by setting parents/children
5. **Add Photos**: Click on a person, then upload photos/documents
6. **Explore**: Zoom, pan, and click around your family tree!

**Need help?** See [FOR_USERS.md](docs/FOR_USERS.md) for complete guide

### Family Tree Navigation

- **Zoom**: Use mouse wheel to zoom in/out
- **Pan**: Click and drag to move around the tree
- **Select**: Click on a member to open their details
- **Colors**:
  - Blue: Male
  - Pink: Female
  - Gray: Unknown
  - Green: Selected member

### Side Panel

- Default width: 20% of screen
- **Resize**: Drag the left edge to adjust width (15% - 50%)
- **Edit**: Click the edit icon to modify member details
- **Delete**: Click the trash icon to remove a member
- **Upload**: Add photos and documents related to the member

### Genealogy Search

The search feature allows you to search multiple genealogy websites:

1. Click "Search" in the navigation bar
2. Fill in available information (name, dates, places)
3. Select sources to search
4. Optional: Enable AI-powered search for enhanced results
5. View results from multiple sources

**Note**: Full integration requires API keys and authentication for each genealogy service.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Family Members
- `GET /api/family-members` - List all members
- `POST /api/family-members` - Create member
- `GET /api/family-members/{id}` - Get member details
- `PUT /api/family-members/{id}` - Update member
- `DELETE /api/family-members/{id}` - Delete member
- `GET /api/family-members/{id}/children` - Get children
- `GET /api/family-members/{id}/ancestors` - Get ancestors

### Documents
- `GET /api/documents` - List documents
- `POST /api/documents` - Upload document
- `GET /api/documents/{id}` - Get document
- `DELETE /api/documents/{id}` - Delete document

### Search
- `POST /api/search/genealogy` - Search genealogy records
- `GET /api/search/history` - Get search history
- `GET /api/search/sources` - List available sources

## AI Integration

The application supports AI-powered search through OpenAI and Anthropic Claude:

- **Query Enhancement**: AI suggests name variations, date ranges, and search strategies
- **Result Analysis**: AI ranks and analyzes search results for accuracy
- **Search Strategy**: AI recommends optimal search approaches

To enable AI features, add your API keys to the `.env` file.

## Genealogy Source Integration

### Supported Sources

1. **Ancestry.com**: Requires API key or authentication
2. **FamilySearch**: Free API available with OAuth
3. **Find My Past**: Requires subscription/API access
4. **MyHeritage**: Requires subscription

### Important Notes

- Most genealogy sites require authentication and may have Terms of Service restrictions on scraping
- API access is preferred and should be used when available
- The scraping functionality is provided as a framework - you must ensure compliance with each site's ToS
- Some sites offer partner APIs which are the recommended integration method

### Setting Up API Access

1. **FamilySearch**:
   - Register for a free developer account at https://www.familysearch.org/developers/
   - Obtain OAuth credentials
   - Add to `.env` file

2. **Ancestry.com**:
   - Contact Ancestry for API access
   - May require partnership agreement

3. **Other Sources**:
   - Check their developer portals for API availability
   - Add credentials to `.env` file

## Security Considerations

- Change the `SECRET_KEY` in `.env` to a strong random value
- Never commit `.env` file to version control
- Use HTTPS in production
- Implement rate limiting for API endpoints
- Regularly update dependencies
- Validate and sanitize all user inputs
- Store API keys securely

## Database Migration

To use PostgreSQL instead of SQLite:

1. Install PostgreSQL
2. Create a database
3. Update `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/ancestree
```
4. The tables will be created automatically on first run

## Production Deployment

### Backend

1. Set environment variables for production
2. Use a production ASGI server (Gunicorn with Uvicorn workers)
3. Set up a reverse proxy (Nginx)
4. Use PostgreSQL instead of SQLite
5. Configure CORS for your domain

Example:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend

1. Build the production bundle:
```bash
npm run build
```

2. Serve the `dist` folder with a web server (Nginx, Apache, etc.)

3. Update API endpoint in production configuration

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is provided as-is for educational and personal use.

## Acknowledgments

- D3.js for tree visualization
- FastAPI for the excellent web framework
- FamilySearch for their free API
- The genealogy community

## Support

For issues and questions, please check:
- API documentation at `/docs`
- GitHub issues
- Project documentation

## Roadmap

Future enhancements:
- [ ] GEDCOM import/export
- [ ] DNA match integration
- [ ] Timeline view
- [ ] Relationship calculator
- [ ] Photo face recognition
- [ ] Collaborative family trees
- [ ] Mobile app
- [ ] Print reports and charts
- [ ] Source citations
- [ ] Research notes and tasks

---

Built with love for family history research.
