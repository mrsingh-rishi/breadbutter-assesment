from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud.crud import gig
from app.schemas.schemas import GigResponse, GigCreate, GigUpdate, GigSearchFilter

router = APIRouter()


@router.post("/", response_model=GigResponse)
def create_gig(
    gig_in: GigCreate,
    db: Session = Depends(get_db)
):
    """Create a new gig."""
    return gig.create(db, gig_in)


@router.get("/", response_model=List[GigResponse])
def get_gigs(
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    db: Session = Depends(get_db)
):
    """Get all gigs with pagination."""
    return gig.get_multi(db, skip=skip, limit=limit)


@router.get("/{gig_id}", response_model=GigResponse)
def get_gig(
    gig_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific gig by ID."""
    db_gig = gig.get(db, gig_id)
    if not db_gig:
        raise HTTPException(status_code=404, detail="Gig not found")
    return db_gig


@router.put("/{gig_id}", response_model=GigResponse)
def update_gig(
    gig_id: str,
    gig_update: GigUpdate,
    db: Session = Depends(get_db)
):
    """Update a gig."""
    db_gig = gig.get(db, gig_id)
    if not db_gig:
        raise HTTPException(status_code=404, detail="Gig not found")
    
    return gig.update(db, db_gig, gig_update)


@router.delete("/{gig_id}")
def delete_gig(
    gig_id: str,
    db: Session = Depends(get_db)
):
    """Delete a gig."""
    db_gig = gig.delete(db, gig_id)
    if not db_gig:
        raise HTTPException(status_code=404, detail="Gig not found")
    return {"message": "Gig deleted successfully"}


@router.post("/search", response_model=List[GigResponse])
def search_gigs(
    filters: GigSearchFilter,
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    db: Session = Depends(get_db)
):
    """Search gigs with filters."""
    return gig.search(db, filters, skip=skip, limit=limit)

