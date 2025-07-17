from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.crud.crud import talent, portfolio_item
from app.schemas.schemas import (
    TalentResponse, TalentCreate, TalentUpdate, TalentSearchFilter,
    PortfolioItemResponse, PortfolioItemCreate
)

router = APIRouter()


@router.post("/", response_model=TalentResponse)
def create_talent(
    talent_in: TalentCreate,
    db: Session = Depends(get_db)
):
    """Create a new talent profile."""
    db_talent = talent.get_by_email(db, email=talent_in.email)
    if db_talent:
        raise HTTPException(
            status_code=400,
            detail="Talent with this email already exists"
        )
    
    return talent.create(db, talent_in)


@router.get("/", response_model=List[TalentResponse])
def get_talents(
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    db: Session = Depends(get_db)
):
    """Get all talents with pagination."""
    return talent.get_multi(db, skip=skip, limit=limit)


@router.get("/{talent_id}", response_model=TalentResponse)
def get_talent(
    talent_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific talent by ID."""
    db_talent = talent.get(db, talent_id)
    if not db_talent:
        raise HTTPException(status_code=404, detail="Talent not found")
    return db_talent


@router.put("/{talent_id}", response_model=TalentResponse)
def update_talent(
    talent_id: str,
    talent_update: TalentUpdate,
    db: Session = Depends(get_db)
):
    """Update a talent profile."""
    db_talent = talent.get(db, talent_id)
    if not db_talent:
        raise HTTPException(status_code=404, detail="Talent not found")
    
    return talent.update(db, db_talent, talent_update)


@router.delete("/{talent_id}")
def delete_talent(
    talent_id: str,
    db: Session = Depends(get_db)
):
    """Delete a talent profile."""
    db_talent = talent.delete(db, talent_id)
    if not db_talent:
        raise HTTPException(status_code=404, detail="Talent not found")
    return {"message": "Talent deleted successfully"}


@router.post("/search", response_model=List[TalentResponse])
def search_talents(
    filters: TalentSearchFilter,
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    db: Session = Depends(get_db)
):
    """Search talents with filters."""
    return talent.search(db, filters, skip=skip, limit=limit)


@router.post("/{talent_id}/portfolio", response_model=PortfolioItemResponse)
def create_portfolio_item(
    talent_id: str,
    portfolio_item_in: PortfolioItemCreate,
    db: Session = Depends(get_db)
):
    """Add a portfolio item to a talent."""
    db_talent = talent.get(db, talent_id)
    if not db_talent:
        raise HTTPException(status_code=404, detail="Talent not found")
    
    return portfolio_item.create(db, portfolio_item_in, talent_id)


@router.get("/{talent_id}/portfolio", response_model=List[PortfolioItemResponse])
def get_talent_portfolio(
    talent_id: str,
    db: Session = Depends(get_db)
):
    """Get all portfolio items for a talent."""
    db_talent = talent.get(db, talent_id)
    if not db_talent:
        raise HTTPException(status_code=404, detail="Talent not found")
    
    return portfolio_item.get_by_talent(db, talent_id)


@router.delete("/portfolio/{portfolio_item_id}")
def delete_portfolio_item(
    portfolio_item_id: str,
    db: Session = Depends(get_db)
):
    """Delete a portfolio item."""
    db_item = portfolio_item.delete(db, portfolio_item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    return {"message": "Portfolio item deleted successfully"}
