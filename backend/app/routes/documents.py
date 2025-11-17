from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from pathlib import Path
import uuid
from datetime import datetime

from ..database import get_db
from ..models import User, Document, FamilyMember
from ..schemas import Document as DocumentSchema
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/documents", tags=["documents"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 10485760))  # 10MB default

# Create upload directories if they don't exist
Path(f"{UPLOAD_DIR}/images").mkdir(parents=True, exist_ok=True)
Path(f"{UPLOAD_DIR}/documents").mkdir(parents=True, exist_ok=True)

def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    """Save uploaded file to destination"""
    with destination.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

@router.post("", response_model=DocumentSchema, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    document_type: Optional[str] = Form(None),
    family_member_id: Optional[int] = Form(None),
    source: Optional[str] = Form("uploaded"),
    source_url: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a document or image"""
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning

    if file_size > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {MAX_UPLOAD_SIZE} bytes"
        )

    # Verify family member belongs to user if provided
    if family_member_id:
        member = db.query(FamilyMember).filter(
            FamilyMember.id == family_member_id,
            FamilyMember.user_id == current_user.id
        ).first()
        if not member:
            raise HTTPException(status_code=404, detail="Family member not found")

    # Determine subdirectory based on file type
    content_type = file.content_type or ""
    if content_type.startswith("image/"):
        subdir = "images"
    else:
        subdir = "documents"

    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = f"{UPLOAD_DIR}/{subdir}/{unique_filename}"

    # Save file
    try:
        save_upload_file(file, Path(file_path))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save file: {str(e)}"
        )

    # Create database record
    db_document = Document(
        user_id=current_user.id,
        family_member_id=family_member_id,
        title=title,
        description=description,
        document_type=document_type,
        file_path=file_path,
        file_type=content_type,
        source=source,
        source_url=source_url
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return db_document

@router.get("", response_model=List[DocumentSchema])
def get_documents(
    family_member_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get documents for current user, optionally filtered by family member"""
    query = db.query(Document).filter(Document.user_id == current_user.id)

    if family_member_id:
        query = query.filter(Document.family_member_id == family_member_id)

    documents = query.offset(skip).limit(limit).all()
    return documents

@router.get("/{document_id}", response_model=DocumentSchema)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific document"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a document"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete file from disk
    try:
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
    except Exception as e:
        print(f"Error deleting file: {e}")

    # Delete database record
    db.delete(document)
    db.commit()

    return None
