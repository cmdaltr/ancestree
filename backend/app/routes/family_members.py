from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, FamilyMember
from ..schemas import FamilyMemberCreate, FamilyMemberUpdate, FamilyMember as FamilyMemberSchema
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/family-members", tags=["family_members"])

@router.post("", response_model=FamilyMemberSchema, status_code=status.HTTP_201_CREATED)
def create_family_member(
    member: FamilyMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new family member"""
    # Verify parent IDs belong to current user if provided
    if member.father_id:
        father = db.query(FamilyMember).filter(
            FamilyMember.id == member.father_id,
            FamilyMember.user_id == current_user.id
        ).first()
        if not father:
            raise HTTPException(status_code=404, detail="Father not found")

    if member.mother_id:
        mother = db.query(FamilyMember).filter(
            FamilyMember.id == member.mother_id,
            FamilyMember.user_id == current_user.id
        ).first()
        if not mother:
            raise HTTPException(status_code=404, detail="Mother not found")

    db_member = FamilyMember(**member.model_dump(), user_id=current_user.id)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_member

@router.get("", response_model=List[FamilyMemberSchema])
def get_family_members(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get all family members for current user"""
    members = db.query(FamilyMember).filter(
        FamilyMember.user_id == current_user.id
    ).offset(skip).limit(limit).all()

    return members

@router.get("/{member_id}", response_model=FamilyMemberSchema)
def get_family_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific family member"""
    member = db.query(FamilyMember).filter(
        FamilyMember.id == member_id,
        FamilyMember.user_id == current_user.id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Family member not found")

    return member

@router.put("/{member_id}", response_model=FamilyMemberSchema)
def update_family_member(
    member_id: int,
    member_update: FamilyMemberUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a family member"""
    db_member = db.query(FamilyMember).filter(
        FamilyMember.id == member_id,
        FamilyMember.user_id == current_user.id
    ).first()

    if not db_member:
        raise HTTPException(status_code=404, detail="Family member not found")

    # Update fields
    update_data = member_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_member, field, value)

    db.commit()
    db.refresh(db_member)

    return db_member

@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_family_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a family member"""
    member = db.query(FamilyMember).filter(
        FamilyMember.id == member_id,
        FamilyMember.user_id == current_user.id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Family member not found")

    db.delete(member)
    db.commit()

    return None

@router.get("/{member_id}/children", response_model=List[FamilyMemberSchema])
def get_children(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get children of a family member"""
    member = db.query(FamilyMember).filter(
        FamilyMember.id == member_id,
        FamilyMember.user_id == current_user.id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Family member not found")

    children = db.query(FamilyMember).filter(
        ((FamilyMember.father_id == member_id) | (FamilyMember.mother_id == member_id)),
        FamilyMember.user_id == current_user.id
    ).all()

    return children

@router.get("/{member_id}/ancestors", response_model=List[FamilyMemberSchema])
def get_ancestors(
    member_id: int,
    generations: int = 3,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get ancestors of a family member up to specified generations"""
    member = db.query(FamilyMember).filter(
        FamilyMember.id == member_id,
        FamilyMember.user_id == current_user.id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Family member not found")

    ancestors = []
    current_generation = [member]

    for _ in range(generations):
        next_generation = []
        for person in current_generation:
            if person.father_id:
                father = db.query(FamilyMember).filter(
                    FamilyMember.id == person.father_id
                ).first()
                if father and father not in ancestors:
                    ancestors.append(father)
                    next_generation.append(father)

            if person.mother_id:
                mother = db.query(FamilyMember).filter(
                    FamilyMember.id == person.mother_id
                ).first()
                if mother and mother not in ancestors:
                    ancestors.append(mother)
                    next_generation.append(mother)

        current_generation = next_generation

    return ancestors
