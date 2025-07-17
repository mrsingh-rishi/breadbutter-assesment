import time
import math
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from geopy.distance import geodesic
from app.models.models import Talent, Gig, MatchResult
from app.crud.crud import talent, gig, match_result
from app.schemas.schemas import MatchResponse, MatchResultResponse, MatchScoreBreakdown
import logging

logger = logging.getLogger(__name__)


class MatchmakingEngine:
    def __init__(self):
        self.score_weights = {
            'location': 0.20,
            'budget': 0.25,
            'skills': 0.30,
            'experience': 0.15,
            'availability': 0.10,
            'portfolio': 0.15,
            'rating': 0.10
        }
        
    def calculate_location_score(self, talent_location: str, gig_location: Optional[str], is_remote: bool) -> float:
        """Calculate location match score"""
        if is_remote:
            return 10.0  # Perfect score for remote work
        
        if not gig_location:
            return 5.0  # Neutral score if no location specified
        
        # Simple string matching for location (in production, use geocoding)
        if talent_location.lower() in gig_location.lower() or gig_location.lower() in talent_location.lower():
            return 10.0
        elif self._is_same_state_or_region(talent_location, gig_location):
            return 7.0
        elif self._is_same_country(talent_location, gig_location):
            return 4.0
        else:
            return 1.0
    
    def calculate_budget_score(self, talent: Talent, gig: Gig) -> float:
        """Calculate budget compatibility score"""
        if not gig.budget_min or not gig.budget_max:
            return 5.0  # Neutral score if no budget specified
        
        gig_budget_avg = (gig.budget_min + gig.budget_max) / 2
        
        # Check different rate types
        talent_rates = []
        if talent.hourly_rate and gig.duration_days:
            estimated_project_rate = talent.hourly_rate * 8 * gig.duration_days  # 8 hours per day
            talent_rates.append(estimated_project_rate)
        
        if talent.daily_rate and gig.duration_days:
            estimated_project_rate = talent.daily_rate * gig.duration_days
            talent_rates.append(estimated_project_rate)
        
        if talent.project_rate_min and talent.project_rate_max:
            talent_avg_rate = (talent.project_rate_min + talent.project_rate_max) / 2
            talent_rates.append(talent_avg_rate)
        
        if not talent_rates:
            return 5.0  # Neutral if no rates available
        
        # Use the rate that's closest to the gig budget
        best_rate = min(talent_rates, key=lambda x: abs(x - gig_budget_avg))
        
        # Score based on budget compatibility
        ratio = best_rate / gig_budget_avg
        if 0.8 <= ratio <= 1.2:  # Within 20% of budget
            return 10.0
        elif 0.6 <= ratio <= 1.4:  # Within 40% of budget
            return 7.0
        elif 0.4 <= ratio <= 1.6:  # Within 60% of budget
            return 4.0
        else:
            return 1.0
    
    def calculate_skills_score(self, talent: Talent, gig: Gig) -> float:
        """Calculate skills match score"""
        if not gig.required_skills:
            return 5.0  # Neutral if no skills specified
        
        talent_skills = {skill.name.lower() for skill in talent.skills}
        required_skills = {skill.name.lower() for skill in gig.required_skills}
        
        if not talent_skills:
            return 0.0
        
        # Calculate skill overlap
        matching_skills = talent_skills.intersection(required_skills)
        skill_match_ratio = len(matching_skills) / len(required_skills)
        
        # Category bonus
        talent_categories = {skill.category.lower() for skill in talent.skills}
        required_categories = {skill.category.lower() for skill in gig.required_skills}
        category_match = len(talent_categories.intersection(required_categories)) / len(required_categories)
        
        # Combined score
        base_score = skill_match_ratio * 10
        category_bonus = category_match * 2
        
        return min(base_score + category_bonus, 10.0)
    
    def calculate_experience_score(self, talent: Talent, gig: Gig) -> float:
        """Calculate experience match score"""
        if not gig.experience_required:
            return 5.0  # Neutral if no experience requirement
        
        experience_mapping = {
            'junior': (0, 2),
            'mid': (2, 5),
            'senior': (5, 100)
        }
        
        required_min, required_max = experience_mapping.get(gig.experience_required, (0, 100))
        
        if required_min <= talent.experience_years <= required_max:
            return 10.0
        elif talent.experience_years >= required_min:
            # Overqualified but acceptable
            return 7.0
        else:
            # Underqualified
            gap = required_min - talent.experience_years
            return max(0, 10 - gap * 2)
    
    def calculate_availability_score(self, talent: Talent, gig: Gig) -> float:
        """Calculate availability score"""
        if talent.availability_status == 'available':
            return 10.0
        elif talent.availability_status == 'busy':
            return 3.0
        else:  # unavailable
            return 0.0
    
    def calculate_portfolio_score(self, talent: Talent, gig: Gig) -> float:
        """Calculate portfolio relevance score"""
        if not talent.portfolio_items:
            return 0.0
        
        portfolio_score = 0.0
        max_items = min(len(talent.portfolio_items), 5)  # Consider up to 5 items
        
        for item in talent.portfolio_items[:max_items]:
            item_score = 0.0
            
            # Project type match
            if item.project_type and gig.category:
                if item.project_type.lower() == gig.category.lower():
                    item_score += 3.0
            
            # Style keywords match
            if item.style_keywords and gig.style_preferences:
                item_keywords = set(item.style_keywords.lower().split(','))
                gig_keywords = set(gig.style_preferences.lower().split())
                
                if item_keywords.intersection(gig_keywords):
                    item_score += 2.0
            
            # Tags match
            if item.tags and gig.description:
                item_tags = set(item.tags.lower().split(','))
                gig_words = set(gig.description.lower().split())
                
                if item_tags.intersection(gig_words):
                    item_score += 1.0
            
            portfolio_score += item_score
        
        return min(portfolio_score / max_items, 10.0)
    
    def calculate_rating_score(self, talent: Talent) -> float:
        """Calculate score based on talent rating"""
        if talent.rating == 0:
            return 5.0  # Neutral for new talent
        
        # Scale 0-5 rating to 0-10 score
        return talent.rating * 2
    
    def calculate_match_score(self, talent: Talent, gig: Gig) -> Tuple[float, MatchScoreBreakdown]:
        """Calculate comprehensive match score"""
        scores = {
            'location': self.calculate_location_score(talent.location, gig.location, gig.is_remote),
            'budget': self.calculate_budget_score(talent, gig),
            'skills': self.calculate_skills_score(talent, gig),
            'experience': self.calculate_experience_score(talent, gig),
            'availability': self.calculate_availability_score(talent, gig),
            'portfolio': self.calculate_portfolio_score(talent, gig),
            'rating': self.calculate_rating_score(talent)
        }
        
        # Calculate weighted score
        total_score = sum(scores[key] * self.score_weights[key] for key in scores)
        
        # Apply priority bonus
        priority_bonus = {'low': 0, 'medium': 0.5, 'high': 1.0}
        total_score += priority_bonus.get(gig.priority, 0)
        
        # Apply success rate bonus
        if talent.success_rate > 0.9:
            total_score += 0.5
        elif talent.success_rate > 0.8:
            total_score += 0.3
        
        total_score = min(total_score, 10.0)
        
        score_breakdown = MatchScoreBreakdown(
            location_score=scores['location'],
            budget_score=scores['budget'],
            skill_score=scores['skills'],
            experience_score=scores['experience'],
            availability_score=scores['availability'],
            portfolio_score=scores['portfolio'],
            rating_score=scores['rating']
        )
        
        return total_score, score_breakdown
    
    def generate_match_explanation(self, talent: Talent, gig: Gig, score_breakdown: MatchScoreBreakdown) -> str:
        """Generate human-readable match explanation"""
        explanations = []
        
        # Location
        if score_breakdown.location_score >= 8:
            explanations.append("Excellent location match")
        elif score_breakdown.location_score >= 6:
            explanations.append("Good location compatibility")
        elif score_breakdown.location_score <= 3:
            explanations.append("Location may require discussion")
        
        # Budget
        if score_breakdown.budget_score >= 8:
            explanations.append("Budget aligns well")
        elif score_breakdown.budget_score >= 6:
            explanations.append("Budget is reasonable")
        elif score_breakdown.budget_score <= 3:
            explanations.append("Budget may need negotiation")
        
        # Skills
        if score_breakdown.skill_score >= 8:
            explanations.append("Strong skill match")
        elif score_breakdown.skill_score >= 6:
            explanations.append("Good skill compatibility")
        elif score_breakdown.skill_score <= 3:
            explanations.append("Limited skill overlap")
        
        # Experience
        if score_breakdown.experience_score >= 8:
            explanations.append("Perfect experience level")
        elif score_breakdown.experience_score >= 6:
            explanations.append("Suitable experience")
        
        # Portfolio
        if score_breakdown.portfolio_score >= 6:
            explanations.append("Relevant portfolio work")
        
        # Rating
        if score_breakdown.rating_score >= 8:
            explanations.append("Highly rated talent")
        elif score_breakdown.rating_score >= 6:
            explanations.append("Good reputation")
        
        return "; ".join(explanations) or "Basic compatibility"
    
    def find_matches(self, db: Session, gig_id: str, limit: int = 10) -> List[MatchResult]:
        """Find and score talent matches for a gig"""
        start_time = time.time()
        
        # Get the gig
        gig_obj = gig.get(db, gig_id)
        if not gig_obj:
            raise ValueError(f"Gig with id {gig_id} not found")
        
        # Get all available talents
        talents = talent.get_multi(db, limit=1000)  # Get more talents for better matching
        
        # Score each talent
        matches = []
        for talent_obj in talents:
            if talent_obj.availability_status == 'unavailable':
                continue
            
            match_score, score_breakdown = self.calculate_match_score(talent_obj, gig_obj)
            
            # Only include matches with score > 3.0
            if match_score > 3.0:
                explanation = self.generate_match_explanation(talent_obj, gig_obj, score_breakdown)
                
                match_data = {
                    'gig_id': gig_id,
                    'talent_id': talent_obj.id,
                    'match_score': match_score,
                    'ranking': 0,  # Will be set later
                    'location_score': score_breakdown.location_score,
                    'budget_score': score_breakdown.budget_score,
                    'skill_score': score_breakdown.skill_score,
                    'experience_score': score_breakdown.experience_score,
                    'availability_score': score_breakdown.availability_score,
                    'portfolio_score': score_breakdown.portfolio_score,
                    'rating_score': score_breakdown.rating_score,
                    'match_explanation': explanation
                }
                
                matches.append((match_score, match_data, talent_obj))
        
        # Sort by score descending
        matches.sort(key=lambda x: x[0], reverse=True)
        
        # Clear existing matches for this gig
        match_result.delete_by_gig(db, gig_id)
        
        # Save top matches
        saved_matches = []
        for i, (score, match_data, talent_obj) in enumerate(matches[:limit]):
            match_data['ranking'] = i + 1
            saved_match = match_result.create(db, match_data)
            saved_matches.append(saved_match)
        
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        logger.info(f"Found {len(saved_matches)} matches for gig {gig_id} in {processing_time:.2f}ms")
        
        return saved_matches
    
    def _is_same_state_or_region(self, location1: str, location2: str) -> bool:
        """Check if two locations are in the same state/region"""
        # Simple implementation - in production, use geocoding service
        common_states = ['mumbai', 'delhi', 'bangalore', 'hyderabad', 'pune', 'chennai', 'kolkata']
        
        for state in common_states:
            if state in location1.lower() and state in location2.lower():
                return True
        
        return False
    
    def _is_same_country(self, location1: str, location2: str) -> bool:
        """Check if two locations are in the same country"""
        # Simple implementation - assume all locations are in India unless specified
        return True


# AI-powered matching (optional enhancement)
class AIMatchmakingEngine(MatchmakingEngine):
    def __init__(self):
        super().__init__()
        self.use_embeddings = False
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.use_embeddings = True
        except ImportError:
            logger.warning("sentence-transformers not available, falling back to rule-based matching")
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        if not self.use_embeddings:
            return 0.0
        
        try:
            embeddings = self.model.encode([text1, text2])
            from sklearn.metrics.pairwise import cosine_similarity
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating semantic similarity: {e}")
            return 0.0
    
    def calculate_enhanced_portfolio_score(self, talent: Talent, gig: Gig) -> float:
        """Enhanced portfolio scoring with AI"""
        base_score = super().calculate_portfolio_score(talent, gig)
        
        if not self.use_embeddings or not talent.portfolio_items:
            return base_score
        
        # Semantic similarity bonus
        semantic_scores = []
        for item in talent.portfolio_items[:5]:
            if item.description:
                similarity = self.calculate_semantic_similarity(
                    item.description,
                    gig.description
                )
                semantic_scores.append(similarity * 5)  # Scale to 0-5
        
        if semantic_scores:
            semantic_bonus = sum(semantic_scores) / len(semantic_scores)
            return min(base_score + semantic_bonus, 10.0)
        
        return base_score


# Create instances
rule_based_engine = MatchmakingEngine()
ai_engine = AIMatchmakingEngine()
