from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class AvailabilityStatus(str, Enum):
    available = "available"
    busy = "busy"
    unavailable = "unavailable"


class ExperienceLevel(str, Enum):
    junior = "junior"
    mid = "mid"
    senior = "senior"


class GigStatus(str, Enum):
    open = "open"
    assigned = "assigned"
    completed = "completed"
    cancelled = "cancelled"


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class FeedbackType(str, Enum):
    match_quality = "match_quality"
    communication = "communication"
    work_quality = "work_quality"


# Base schemas
class SkillBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ClientBase(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PortfolioItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    media_url: Optional[str] = None
    media_type: Optional[str] = None
    project_type: Optional[str] = None
    client_name: Optional[str] = None
    completion_date: Optional[datetime] = None
    tags: Optional[str] = None
    style_keywords: Optional[str] = None


class PortfolioItemCreate(PortfolioItemBase):
    pass


class PortfolioItemResponse(PortfolioItemBase):
    id: str
    talent_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TalentBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    location: str
    bio: Optional[str] = None
    experience_years: int = 0
    hourly_rate: Optional[float] = None
    daily_rate: Optional[float] = None
    project_rate_min: Optional[float] = None
    project_rate_max: Optional[float] = None
    availability_status: AvailabilityStatus = AvailabilityStatus.available
    portfolio_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    instagram_url: Optional[str] = None
    website_url: Optional[str] = None


class TalentCreate(TalentBase):
    skill_ids: List[str] = []


class TalentUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    experience_years: Optional[int] = None
    hourly_rate: Optional[float] = None
    daily_rate: Optional[float] = None
    project_rate_min: Optional[float] = None
    project_rate_max: Optional[float] = None
    availability_status: Optional[AvailabilityStatus] = None
    portfolio_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    instagram_url: Optional[str] = None
    website_url: Optional[str] = None
    skill_ids: Optional[List[str]] = None


class TalentResponse(TalentBase):
    id: str
    rating: float
    total_projects: int
    success_rate: float
    response_time_hours: float
    created_at: datetime
    updated_at: datetime
    skills: List[SkillResponse] = []
    portfolio_items: List[PortfolioItemResponse] = []
    
    class Config:
        from_attributes = True


class GigBase(BaseModel):
    title: str
    description: str
    category: str
    location: Optional[str] = None
    is_remote: bool = False
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    duration_days: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    style_preferences: Optional[str] = None
    deliverables: Optional[str] = None
    experience_required: Optional[ExperienceLevel] = None
    priority: Priority = Priority.medium


class GigCreate(GigBase):
    client_id: str
    required_skill_ids: List[str] = []


class GigUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    is_remote: Optional[bool] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    duration_days: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    style_preferences: Optional[str] = None
    deliverables: Optional[str] = None
    experience_required: Optional[ExperienceLevel] = None
    status: Optional[GigStatus] = None
    priority: Optional[Priority] = None
    required_skill_ids: Optional[List[str]] = None


class GigResponse(GigBase):
    id: str
    client_id: str
    status: GigStatus
    created_at: datetime
    updated_at: datetime
    client: ClientResponse
    required_skills: List[SkillResponse] = []
    
    class Config:
        from_attributes = True


class MatchScoreBreakdown(BaseModel):
    location_score: float
    budget_score: float
    skill_score: float
    experience_score: float
    availability_score: float
    portfolio_score: float
    rating_score: float


class MatchResultResponse(BaseModel):
    id: str
    gig_id: str
    talent_id: str
    match_score: float
    ranking: int
    score_breakdown: MatchScoreBreakdown
    match_explanation: str
    created_at: datetime
    talent: TalentResponse
    
    class Config:
        from_attributes = True


class MatchRequest(BaseModel):
    gig_id: str
    limit: int = Field(default=10, ge=1, le=50)
    use_ai: bool = False


class MatchResponse(BaseModel):
    gig: GigResponse
    matches: List[MatchResultResponse]
    total_matches: int
    algorithm_used: str
    processing_time_ms: float


class MatchFeedbackCreate(BaseModel):
    client_id: str
    talent_id: str
    gig_id: str
    rating: int = Field(ge=1, le=5)
    feedback_text: Optional[str] = None
    feedback_type: FeedbackType


class MatchFeedbackResponse(BaseModel):
    id: str
    client_id: str
    talent_id: str
    gig_id: str
    rating: int
    feedback_text: Optional[str]
    feedback_type: FeedbackType
    created_at: datetime
    
    class Config:
        from_attributes = True


class TalentSearchFilter(BaseModel):
    location: Optional[str] = None
    category: Optional[str] = None
    min_experience: Optional[int] = None
    max_experience: Optional[int] = None
    min_rate: Optional[float] = None
    max_rate: Optional[float] = None
    availability_status: Optional[AvailabilityStatus] = None
    skills: Optional[List[str]] = None
    min_rating: Optional[float] = None


class GigSearchFilter(BaseModel):
    category: Optional[str] = None
    location: Optional[str] = None
    is_remote: Optional[bool] = None
    min_budget: Optional[float] = None
    max_budget: Optional[float] = None
    status: Optional[GigStatus] = None
    client_id: Optional[str] = None


class StatsResponse(BaseModel):
    total_talents: int
    total_clients: int
    total_gigs: int
    total_matches: int
    active_gigs: int
    available_talents: int
    avg_match_score: float
    top_categories: List[Dict[str, Any]]
    recent_activity: List[Dict[str, Any]]
