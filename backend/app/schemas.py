from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Family Member Schemas
class FamilyMemberBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    maiden_name: Optional[str] = None
    gender: Gender = Gender.UNKNOWN
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    death_date: Optional[date] = None
    death_place: Optional[str] = None
    burial_place: Optional[str] = None
    occupation: Optional[str] = None
    biography: Optional[str] = None
    notes: Optional[str] = None
    father_id: Optional[int] = None
    mother_id: Optional[int] = None

class FamilyMemberCreate(FamilyMemberBase):
    pass

class FamilyMemberUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    maiden_name: Optional[str] = None
    gender: Optional[Gender] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    death_date: Optional[date] = None
    death_place: Optional[str] = None
    burial_place: Optional[str] = None
    occupation: Optional[str] = None
    biography: Optional[str] = None
    notes: Optional[str] = None
    father_id: Optional[int] = None
    mother_id: Optional[int] = None

class FamilyMember(FamilyMemberBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Marriage Schemas
class MarriageBase(BaseModel):
    person1_id: int
    person2_id: int
    marriage_date: Optional[date] = None
    marriage_place: Optional[str] = None
    divorce_date: Optional[date] = None
    notes: Optional[str] = None

class MarriageCreate(MarriageBase):
    pass

class Marriage(MarriageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Document Schemas
class DocumentBase(BaseModel):
    title: str
    description: Optional[str] = None
    document_type: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    family_member_id: Optional[int] = None

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    user_id: int
    file_path: str
    file_type: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Search Schemas
class SearchQuery(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_year: Optional[int] = None
    birth_place: Optional[str] = None
    death_year: Optional[int] = None
    death_place: Optional[str] = None
    use_ai: bool = False
    sources: List[str] = ["ancestry", "familysearch", "findmypast", "myheritage"]

class SearchResult(BaseModel):
    source: str
    name: str
    birth_date: Optional[str] = None
    birth_place: Optional[str] = None
    death_date: Optional[str] = None
    death_place: Optional[str] = None
    url: Optional[str] = None
    confidence_score: Optional[float] = None
    additional_info: Optional[dict] = None
