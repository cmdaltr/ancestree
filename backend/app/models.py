from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    family_members = relationship("FamilyMember", back_populates="owner")
    documents = relationship("Document", back_populates="owner")

class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Basic Information
    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    last_name = Column(String, nullable=False)
    maiden_name = Column(String)
    gender = Column(Enum(Gender), default=Gender.UNKNOWN)

    # Dates
    birth_date = Column(Date)
    birth_place = Column(String)
    death_date = Column(Date)
    death_place = Column(String)
    burial_place = Column(String)

    # Additional Information
    occupation = Column(String)
    biography = Column(Text)
    notes = Column(Text)

    # Relationships
    father_id = Column(Integer, ForeignKey("family_members.id"), nullable=True)
    mother_id = Column(Integer, ForeignKey("family_members.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # SQLAlchemy Relationships
    owner = relationship("User", back_populates="family_members")
    father = relationship("FamilyMember", foreign_keys=[father_id], remote_side="FamilyMember.id", backref="children_as_father")
    mother = relationship("FamilyMember", foreign_keys=[mother_id], remote_side="FamilyMember.id", backref="children_as_mother")
    documents = relationship("Document", back_populates="family_member")
    marriages = relationship("Marriage", foreign_keys="Marriage.person1_id", back_populates="person1")
    marriages_as_spouse = relationship("Marriage", foreign_keys="Marriage.person2_id", back_populates="person2")

class Marriage(Base):
    __tablename__ = "marriages"

    id = Column(Integer, primary_key=True, index=True)
    person1_id = Column(Integer, ForeignKey("family_members.id"), nullable=False)
    person2_id = Column(Integer, ForeignKey("family_members.id"), nullable=False)

    marriage_date = Column(Date)
    marriage_place = Column(String)
    divorce_date = Column(Date)
    notes = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    person1 = relationship("FamilyMember", foreign_keys=[person1_id], back_populates="marriages")
    person2 = relationship("FamilyMember", foreign_keys=[person2_id], back_populates="marriages_as_spouse")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    family_member_id = Column(Integer, ForeignKey("family_members.id"), nullable=True)

    title = Column(String, nullable=False)
    description = Column(Text)
    document_type = Column(String)  # birth_certificate, death_certificate, photo, etc.
    file_path = Column(String, nullable=False)
    file_type = Column(String)  # image/jpeg, application/pdf, etc.

    # Source information
    source = Column(String)  # ancestry.com, familysearch, uploaded, etc.
    source_url = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="documents")
    family_member = relationship("FamilyMember", back_populates="documents")

class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    query = Column(String, nullable=False)
    search_type = Column(String)  # manual, ai_assisted, api
    results_count = Column(Integer, default=0)
    sources_searched = Column(String)  # JSON string of sources

    created_at = Column(DateTime, default=datetime.utcnow)
