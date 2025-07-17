from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud.crud import skill
from app.schemas.schemas import SkillResponse, SkillCreate

router = APIRouter()


@router.post("/", response_model=SkillResponse)
def create_skill(
    skill_in: SkillCreate,
    db: Session = Depends(get_db)
):
    """Create a new skill."""
    db_skill = skill.get_by_name(db, name=skill_in.name)
    if db_skill:
        raise HTTPException(
            status_code=400,
            detail="Skill with this name already exists"
        )
    
    return skill.create(db, skill_in)


@router.get("/", response_model=List[SkillResponse])
def get_skills(
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    category: str = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """Get all skills with optional category filter."""
    if category:
        return skill.get_by_category(db, category)
    return skill.get_multi(db, skip=skip, limit=limit)


@router.get("/{skill_id}", response_model=SkillResponse)
def get_skill(
    skill_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific skill by ID."""
    db_skill = skill.get(db, skill_id)
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return db_skill


@router.get("/categories/list")
def get_skill_categories(db: Session = Depends(get_db)):
    """Get all unique skill categories."""
    from sqlalchemy import distinct
    from app.models.models import Skill
    
    categories = db.query(distinct(Skill.category)).all()
    return {"categories": [category[0] for category in categories]}
