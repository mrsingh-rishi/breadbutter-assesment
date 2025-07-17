from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from app.models.models import (
    Client, Talent, Skill, PortfolioItem, Gig, MatchResult, MatchFeedback,
    talent_skills, gig_skills
)
from app.schemas.schemas import (
    ClientCreate, TalentCreate, TalentUpdate, SkillCreate,
    PortfolioItemCreate, GigCreate, GigUpdate, MatchFeedbackCreate,
    TalentSearchFilter, GigSearchFilter
)


class CRUDClient:
    def create(self, db: Session, obj_in: ClientCreate) -> Client:
        db_obj = Client(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: str) -> Optional[Client]:
        return db.query(Client).filter(Client.id == id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[Client]:
        return db.query(Client).filter(Client.email == email).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Client]:
        return db.query(Client).offset(skip).limit(limit).all()

    def update(self, db: Session, db_obj: Client, obj_in: dict) -> Client:
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: str) -> Optional[Client]:
        obj = db.query(Client).filter(Client.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


class CRUDSkill:
    def create(self, db: Session, obj_in: SkillCreate) -> Skill:
        db_obj = Skill(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: str) -> Optional[Skill]:
        return db.query(Skill).filter(Skill.id == id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[Skill]:
        return db.query(Skill).filter(Skill.name == name).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Skill]:
        return db.query(Skill).offset(skip).limit(limit).all()

    def get_by_category(self, db: Session, category: str) -> List[Skill]:
        return db.query(Skill).filter(Skill.category == category).all()

    def get_by_ids(self, db: Session, ids: List[str]) -> List[Skill]:
        return db.query(Skill).filter(Skill.id.in_(ids)).all()


class CRUDTalent:
    def create(self, db: Session, obj_in: TalentCreate) -> Talent:
        # Create talent without skills first
        talent_data = obj_in.dict()
        skill_ids = talent_data.pop('skill_ids', [])
        
        db_obj = Talent(**talent_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Add skills if provided
        if skill_ids:
            skills = db.query(Skill).filter(Skill.id.in_(skill_ids)).all()
            db_obj.skills = skills
            db.commit()
            db.refresh(db_obj)
        
        return db_obj

    def get(self, db: Session, id: str) -> Optional[Talent]:
        return db.query(Talent).filter(Talent.id == id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[Talent]:
        return db.query(Talent).filter(Talent.email == email).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Talent]:
        return db.query(Talent).offset(skip).limit(limit).all()

    def search(self, db: Session, filters: TalentSearchFilter, skip: int = 0, limit: int = 100) -> List[Talent]:
        query = db.query(Talent)
        
        if filters.location:
            query = query.filter(Talent.location.ilike(f"%{filters.location}%"))
        
        if filters.min_experience is not None:
            query = query.filter(Talent.experience_years >= filters.min_experience)
        
        if filters.max_experience is not None:
            query = query.filter(Talent.experience_years <= filters.max_experience)
        
        if filters.min_rate is not None:
            query = query.filter(
                or_(
                    Talent.hourly_rate >= filters.min_rate,
                    Talent.daily_rate >= filters.min_rate,
                    Talent.project_rate_min >= filters.min_rate
                )
            )
        
        if filters.max_rate is not None:
            query = query.filter(
                or_(
                    Talent.hourly_rate <= filters.max_rate,
                    Talent.daily_rate <= filters.max_rate,
                    Talent.project_rate_max <= filters.max_rate
                )
            )
        
        if filters.availability_status:
            query = query.filter(Talent.availability_status == filters.availability_status)
        
        if filters.min_rating is not None:
            query = query.filter(Talent.rating >= filters.min_rating)
        
        if filters.skills:
            query = query.join(Talent.skills).filter(Skill.name.in_(filters.skills))
        
        if filters.category:
            query = query.join(Talent.skills).filter(Skill.category == filters.category)
        
        return query.offset(skip).limit(limit).all()

    def update(self, db: Session, db_obj: Talent, obj_in: TalentUpdate) -> Talent:
        update_data = obj_in.dict(exclude_unset=True)
        skill_ids = update_data.pop('skill_ids', None)
        
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        if skill_ids is not None:
            skills = db.query(Skill).filter(Skill.id.in_(skill_ids)).all()
            db_obj.skills = skills
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: str) -> Optional[Talent]:
        obj = db.query(Talent).filter(Talent.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


class CRUDPortfolioItem:
    def create(self, db: Session, obj_in: PortfolioItemCreate, talent_id: str) -> PortfolioItem:
        db_obj = PortfolioItem(**obj_in.dict(), talent_id=talent_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: str) -> Optional[PortfolioItem]:
        return db.query(PortfolioItem).filter(PortfolioItem.id == id).first()

    def get_by_talent(self, db: Session, talent_id: str) -> List[PortfolioItem]:
        return db.query(PortfolioItem).filter(PortfolioItem.talent_id == talent_id).all()

    def delete(self, db: Session, id: str) -> Optional[PortfolioItem]:
        obj = db.query(PortfolioItem).filter(PortfolioItem.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


class CRUDGig:
    def create(self, db: Session, obj_in: GigCreate) -> Gig:
        gig_data = obj_in.dict()
        skill_ids = gig_data.pop('required_skill_ids', [])
        
        db_obj = Gig(**gig_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Add required skills
        if skill_ids:
            skills = db.query(Skill).filter(Skill.id.in_(skill_ids)).all()
            db_obj.required_skills = skills
            db.commit()
            db.refresh(db_obj)
        
        return db_obj

    def get(self, db: Session, id: str) -> Optional[Gig]:
        return db.query(Gig).filter(Gig.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Gig]:
        return db.query(Gig).offset(skip).limit(limit).all()

    def search(self, db: Session, filters: GigSearchFilter, skip: int = 0, limit: int = 100) -> List[Gig]:
        query = db.query(Gig)
        
        if filters.category:
            query = query.filter(Gig.category == filters.category)
        
        if filters.location:
            query = query.filter(Gig.location.ilike(f"%{filters.location}%"))
        
        if filters.is_remote is not None:
            query = query.filter(Gig.is_remote == filters.is_remote)
        
        if filters.min_budget is not None:
            query = query.filter(Gig.budget_min >= filters.min_budget)
        
        if filters.max_budget is not None:
            query = query.filter(Gig.budget_max <= filters.max_budget)
        
        if filters.status:
            query = query.filter(Gig.status == filters.status)
        
        if filters.client_id:
            query = query.filter(Gig.client_id == filters.client_id)
        
        return query.offset(skip).limit(limit).all()

    def update(self, db: Session, db_obj: Gig, obj_in: GigUpdate) -> Gig:
        update_data = obj_in.dict(exclude_unset=True)
        skill_ids = update_data.pop('required_skill_ids', None)
        
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        if skill_ids is not None:
            skills = db.query(Skill).filter(Skill.id.in_(skill_ids)).all()
            db_obj.required_skills = skills
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: str) -> Optional[Gig]:
        obj = db.query(Gig).filter(Gig.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


class CRUDMatchResult:
    def create(self, db: Session, match_data: dict) -> MatchResult:
        db_obj = MatchResult(**match_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_gig(self, db: Session, gig_id: str) -> List[MatchResult]:
        return db.query(MatchResult).filter(MatchResult.gig_id == gig_id).order_by(MatchResult.ranking).all()

    def get_by_talent(self, db: Session, talent_id: str) -> List[MatchResult]:
        return db.query(MatchResult).filter(MatchResult.talent_id == talent_id).all()

    def delete_by_gig(self, db: Session, gig_id: str) -> int:
        count = db.query(MatchResult).filter(MatchResult.gig_id == gig_id).count()
        db.query(MatchResult).filter(MatchResult.gig_id == gig_id).delete()
        db.commit()
        return count


class CRUDMatchFeedback:
    def create(self, db: Session, obj_in: MatchFeedbackCreate) -> MatchFeedback:
        db_obj = MatchFeedback(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_gig(self, db: Session, gig_id: str) -> List[MatchFeedback]:
        return db.query(MatchFeedback).filter(MatchFeedback.gig_id == gig_id).all()

    def get_by_talent(self, db: Session, talent_id: str) -> List[MatchFeedback]:
        return db.query(MatchFeedback).filter(MatchFeedback.talent_id == talent_id).all()

    def get_by_client(self, db: Session, client_id: str) -> List[MatchFeedback]:
        return db.query(MatchFeedback).filter(MatchFeedback.client_id == client_id).all()


class CRUDStats:
    def get_dashboard_stats(self, db: Session) -> Dict[str, Any]:
        total_talents = db.query(Talent).count()
        total_clients = db.query(Client).count()
        total_gigs = db.query(Gig).count()
        total_matches = db.query(MatchResult).count()
        active_gigs = db.query(Gig).filter(Gig.status == "open").count()
        available_talents = db.query(Talent).filter(Talent.availability_status == "available").count()
        
        avg_match_score = db.query(func.avg(MatchResult.match_score)).scalar() or 0.0
        
        # Top categories
        top_categories = db.query(
            Gig.category,
            func.count(Gig.id).label('count')
        ).group_by(Gig.category).order_by(func.count(Gig.id).desc()).limit(5).all()
        
        # Recent activity (last 10 gigs)
        recent_gigs = db.query(Gig).order_by(Gig.created_at.desc()).limit(10).all()
        recent_activity = [
            {
                "type": "gig_created",
                "title": gig.title,
                "category": gig.category,
                "created_at": gig.created_at
            }
            for gig in recent_gigs
        ]
        
        return {
            "total_talents": total_talents,
            "total_clients": total_clients,
            "total_gigs": total_gigs,
            "total_matches": total_matches,
            "active_gigs": active_gigs,
            "available_talents": available_talents,
            "avg_match_score": round(avg_match_score, 2),
            "top_categories": [{"category": cat[0], "count": cat[1]} for cat in top_categories],
            "recent_activity": recent_activity
        }


# Create instances
client = CRUDClient()
skill = CRUDSkill()
talent = CRUDTalent()
portfolio_item = CRUDPortfolioItem()
gig = CRUDGig()
match_result = CRUDMatchResult()
match_feedback = CRUDMatchFeedback()
stats = CRUDStats()
