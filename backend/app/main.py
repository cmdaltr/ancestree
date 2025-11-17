from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .database import init_db
from .routes import auth, family_members, documents, search

app = FastAPI(
    title="Ancestree API",
    description="API for managing family tree data with AI-powered genealogy search",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for serving files
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
if os.path.exists(UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router)
app.include_router(family_members.router)
app.include_router(documents.router)
app.include_router(search.router)

@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    init_db()

@app.get("/")
def root():
    return {
        "message": "Ancestree API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
