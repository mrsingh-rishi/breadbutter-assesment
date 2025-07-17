from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.crud import stats
from app.schemas.schemas import StatsResponse

router = APIRouter()


@router.get("/dashboard", response_model=StatsResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get comprehensive dashboard statistics."""
    return stats.get_dashboard_stats(db)


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Talent Matchmaking Engine is running"}
