from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String as SQLString


# Association table for many-to-many relationship between talent and skills
talent_skills = Table(
    'talent_skills',
    Base.metadata,
    Column('talent_id', String, ForeignKey('talents.id'), primary_key=True),
    Column('skill_id', String, ForeignKey('skills.id'), primary_key=True)
)

# Association table for many-to-many relationship between gig and required skills
gig_skills = Table(
    'gig_skills',
    Base.metadata,
    Column('gig_id', String, ForeignKey('gigs.id'), primary_key=True),
    Column('skill_id', String, ForeignKey('skills.id'), primary_key=True)
)


class Client(Base):
    __tablename__ = "clients"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    company = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    gigs = relationship("Gig", back_populates="client")
    match_feedback = relationship("MatchFeedback", back_populates="client")


class Talent(Base):
    __tablename__ = "talents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    experience_years = Column(Integer, default=0)
    hourly_rate = Column(Float, nullable=True)
    daily_rate = Column(Float, nullable=True)
    project_rate_min = Column(Float, nullable=True)
    project_rate_max = Column(Float, nullable=True)
    availability_status = Column(String, default="available")  # available, busy, unavailable
    rating = Column(Float, default=0.0)
    total_projects = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    response_time_hours = Column(Float, default=24.0)
    portfolio_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    instagram_url = Column(String, nullable=True)
    website_url = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    skills = relationship("Skill", secondary=talent_skills, back_populates="talents")
    portfolio_items = relationship("PortfolioItem", back_populates="talent")
    match_results = relationship("MatchResult", back_populates="talent")
    match_feedback = relationship("MatchFeedback", back_populates="talent")


class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)  # e.g., "photography", "design", "video"
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    talents = relationship("Talent", secondary=talent_skills, back_populates="skills")
    gigs = relationship("Gig", secondary=gig_skills, back_populates="required_skills")


class PortfolioItem(Base):
    __tablename__ = "portfolio_items"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    talent_id = Column(String, ForeignKey("talents.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    media_url = Column(String, nullable=True)
    media_type = Column(String, nullable=True)  # image, video, document
    project_type = Column(String, nullable=True)
    client_name = Column(String, nullable=True)
    completion_date = Column(DateTime, nullable=True)
    tags = Column(String, nullable=True)  # comma-separated tags
    style_keywords = Column(String, nullable=True)  # for AI matching
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    talent = relationship("Talent", back_populates="portfolio_items")


class Gig(Base):
    __tablename__ = "gigs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=False)  # photography, design, video, etc.
    location = Column(String, nullable=True)
    is_remote = Column(Boolean, default=False)
    budget_min = Column(Float, nullable=True)
    budget_max = Column(Float, nullable=True)
    duration_days = Column(Integer, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    style_preferences = Column(Text, nullable=True)  # pastel tones, candid portraits, etc.
    deliverables = Column(Text, nullable=True)
    experience_required = Column(String, nullable=True)  # junior, mid, senior
    status = Column(String, default="open")  # open, assigned, completed, cancelled
    priority = Column(String, default="medium")  # low, medium, high
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    client = relationship("Client", back_populates="gigs")
    required_skills = relationship("Skill", secondary=gig_skills, back_populates="gigs")
    match_results = relationship("MatchResult", back_populates="gig")


class MatchResult(Base):
    __tablename__ = "match_results"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    gig_id = Column(String, ForeignKey("gigs.id"), nullable=False)
    talent_id = Column(String, ForeignKey("talents.id"), nullable=False)
    match_score = Column(Float, nullable=False)
    ranking = Column(Integer, nullable=False)
    
    # Score breakdown
    location_score = Column(Float, default=0.0)
    budget_score = Column(Float, default=0.0)
    skill_score = Column(Float, default=0.0)
    experience_score = Column(Float, default=0.0)
    availability_score = Column(Float, default=0.0)
    portfolio_score = Column(Float, default=0.0)
    rating_score = Column(Float, default=0.0)
    
    # Explanation
    match_explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    gig = relationship("Gig", back_populates="match_results")
    talent = relationship("Talent", back_populates="match_results")


class MatchFeedback(Base):
    __tablename__ = "match_feedback"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    talent_id = Column(String, ForeignKey("talents.id"), nullable=False)
    gig_id = Column(String, ForeignKey("gigs.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    feedback_text = Column(Text, nullable=True)
    feedback_type = Column(String, nullable=False)  # match_quality, communication, work_quality
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    client = relationship("Client", back_populates="match_feedback")
    talent = relationship("Talent", back_populates="match_feedback")
    gig = relationship("Gig")
