from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import time
from app.core.database import get_db
from app.crud.crud import gig, match_result, match_feedback
from app.schemas.schemas import (
    MatchRequest, MatchResponse, MatchResultResponse, MatchScoreBreakdown,
    MatchFeedbackCreate, MatchFeedbackResponse
)
from app.services.matchmaking import rule_based_engine, ai_engine
from app.models.models import MatchResult

router = APIRouter()


def convert_match_result_to_response(match_result: MatchResult) -> MatchResultResponse:
    """Convert MatchResult model to MatchResultResponse schema."""
    score_breakdown = MatchScoreBreakdown(
        location_score=match_result.location_score,
        budget_score=match_result.budget_score,
        skill_score=match_result.skill_score,
        experience_score=match_result.experience_score,
        availability_score=match_result.availability_score,
        portfolio_score=match_result.portfolio_score,
        rating_score=match_result.rating_score
    )
    
    return MatchResultResponse(
        id=match_result.id,
        gig_id=match_result.gig_id,
        talent_id=match_result.talent_id,
        match_score=match_result.match_score,
        ranking=match_result.ranking,
        score_breakdown=score_breakdown,
        match_explanation=match_result.match_explanation,
        created_at=match_result.created_at,
        talent=match_result.talent
    )


@router.post("/find-matches", response_model=MatchResponse)
def find_matches(
    request: MatchRequest,
    db: Session = Depends(get_db)
):
    """Find talent matches for a gig using the matchmaking algorithm."""
    start_time = time.time()
    
    # Get the gig
    db_gig = gig.get(db, request.gig_id)
    if not db_gig:
        raise HTTPException(status_code=404, detail="Gig not found")
    
    # Choose the appropriate engine
    engine = ai_engine if request.use_ai else rule_based_engine
    algorithm_used = "AI-Enhanced" if request.use_ai else "Rule-Based"
    
    try:
        # Find matches
        matches = engine.find_matches(db, request.gig_id, request.limit)
        
        # Convert to response format
        match_responses = [convert_match_result_to_response(match) for match in matches]
        
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return MatchResponse(
            gig=db_gig,
            matches=match_responses,
            total_matches=len(matches),
            algorithm_used=algorithm_used,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding matches: {str(e)}")


@router.get("/gig/{gig_id}/matches", response_model=List[MatchResultResponse])
def get_gig_matches(
    gig_id: str,
    db: Session = Depends(get_db)
):
    """Get existing matches for a gig."""
    db_gig = gig.get(db, gig_id)
    if not db_gig:
        raise HTTPException(status_code=404, detail="Gig not found")
    
    matches = match_result.get_by_gig(db, gig_id)
    return [convert_match_result_to_response(match) for match in matches]


@router.get("/talent/{talent_id}/matches", response_model=List[MatchResultResponse])
def get_talent_matches(
    talent_id: str,
    db: Session = Depends(get_db)
):
    """Get matches for a specific talent."""
    matches = match_result.get_by_talent(db, talent_id)
    return [convert_match_result_to_response(match) for match in matches]


@router.post("/feedback", response_model=MatchFeedbackResponse)
def submit_feedback(
    feedback: MatchFeedbackCreate,
    db: Session = Depends(get_db)
):
    """Submit feedback on a match."""
    return match_feedback.create(db, feedback)


@router.get("/feedback/gig/{gig_id}", response_model=List[MatchFeedbackResponse])
def get_gig_feedback(
    gig_id: str,
    db: Session = Depends(get_db)
):
    """Get all feedback for a gig."""
    return match_feedback.get_by_gig(db, gig_id)


@router.get("/feedback/talent/{talent_id}", response_model=List[MatchFeedbackResponse])
def get_talent_feedback(
    talent_id: str,
    db: Session = Depends(get_db)
):
    """Get all feedback for a talent."""
    return match_feedback.get_by_talent(db, talent_id)


@router.get("/feedback/client/{client_id}", response_model=List[MatchFeedbackResponse])
def get_client_feedback(
    client_id: str,
    db: Session = Depends(get_db)
):
    """Get all feedback submitted by a client."""
    return match_feedback.get_by_client(db, client_id)


@router.post("/rematch/{gig_id}")
def rematch_gig(
    gig_id: str,
    background_tasks: BackgroundTasks,
    use_ai: bool = False,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Trigger a rematch for a gig in the background."""
    db_gig = gig.get(db, gig_id)
    if not db_gig:
        raise HTTPException(status_code=404, detail="Gig not found")
    
    def run_rematch():
        engine = ai_engine if use_ai else rule_based_engine
        engine.find_matches(db, gig_id, limit)
    
    background_tasks.add_task(run_rematch)
    return {"message": "Rematch started in background"}
