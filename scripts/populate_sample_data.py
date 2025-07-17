#!/usr/bin/env python3
"""
Script to populate the database with sample data for testing the matchmaking engine.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine
from app.models.models import Base
from app.crud.crud import client, talent, skill, gig, portfolio_item
from app.schemas.schemas import (
    ClientCreate, TalentCreate, SkillCreate, GigCreate, PortfolioItemCreate
)
from datetime import datetime, timedelta
import random

# Create tables
Base.metadata.create_all(bind=engine)

def create_sample_data():
    db = SessionLocal()
    
    try:
        # Create skills
        skills_data = [
            # Photography skills
            {"name": "Portrait Photography", "category": "photography", "description": "Professional portrait photography"},
            {"name": "Landscape Photography", "category": "photography", "description": "Landscape and nature photography"},
            {"name": "Wedding Photography", "category": "photography", "description": "Wedding and event photography"},
            {"name": "Product Photography", "category": "photography", "description": "Commercial product photography"},
            {"name": "Fashion Photography", "category": "photography", "description": "Fashion and lifestyle photography"},
            {"name": "Street Photography", "category": "photography", "description": "Urban and street photography"},
            
            # Design skills
            {"name": "Graphic Design", "category": "design", "description": "Visual design and branding"},
            {"name": "UI/UX Design", "category": "design", "description": "User interface and experience design"},
            {"name": "Brand Identity", "category": "design", "description": "Brand identity and logo design"},
            {"name": "Print Design", "category": "design", "description": "Print and publication design"},
            {"name": "Illustration", "category": "design", "description": "Digital and traditional illustration"},
            
            # Video skills
            {"name": "Video Editing", "category": "video", "description": "Video editing and post-production"},
            {"name": "Motion Graphics", "category": "video", "description": "Animation and motion graphics"},
            {"name": "Cinematography", "category": "video", "description": "Film and video production"},
            {"name": "Color Grading", "category": "video", "description": "Color correction and grading"},
            
            # Marketing skills
            {"name": "Social Media Marketing", "category": "marketing", "description": "Social media strategy and management"},
            {"name": "Content Writing", "category": "marketing", "description": "Creative and marketing content writing"},
            {"name": "SEO", "category": "marketing", "description": "Search engine optimization"},
        ]
        
        created_skills = {}
        for skill_data in skills_data:
            skill_obj = skill.create(db, SkillCreate(**skill_data))
            created_skills[skill_data["name"]] = skill_obj.id
            print(f"Created skill: {skill_data['name']}")
        
        # Create clients
        clients_data = [
            {
                "name": "TechStart Inc.",
                "email": "contact@techstart.com",
                "company": "TechStart Inc.",
                "industry": "Technology",
                "location": "Bangalore"
            },
            {
                "name": "Fashion Forward",
                "email": "hello@fashionforward.com",
                "company": "Fashion Forward",
                "industry": "Fashion",
                "location": "Mumbai"
            },
            {
                "name": "Green Earth Co.",
                "email": "info@greenearth.com",
                "company": "Green Earth Co.",
                "industry": "Sustainability",
                "location": "Delhi"
            },
            {
                "name": "Creative Agency",
                "email": "team@creativeagency.com",
                "company": "Creative Agency",
                "industry": "Marketing",
                "location": "Pune"
            },
            {
                "name": "Wedding Planners",
                "email": "contact@weddingplanners.com",
                "company": "Wedding Planners",
                "industry": "Events",
                "location": "Goa"
            }
        ]
        
        created_clients = {}
        for client_data in clients_data:
            client_obj = client.create(db, ClientCreate(**client_data))
            created_clients[client_data["name"]] = client_obj.id
            print(f"Created client: {client_data['name']}")
        
        # Create talents
        talents_data = [
            {
                "name": "Arjun Sharma",
                "email": "arjun@example.com",
                "location": "Mumbai",
                "bio": "Professional photographer with 5+ years experience in fashion and portrait photography",
                "experience_years": 5,
                "hourly_rate": 2000,
                "daily_rate": 15000,
                "project_rate_min": 25000,
                "project_rate_max": 100000,
                "availability_status": "available",
                "rating": 4.8,
                "total_projects": 45,
                "success_rate": 0.95,
                "skill_ids": [created_skills["Fashion Photography"], created_skills["Portrait Photography"]]
            },
            {
                "name": "Priya Mehta",
                "email": "priya@example.com",
                "location": "Bangalore",
                "bio": "UI/UX designer specializing in mobile apps and web design",
                "experience_years": 3,
                "hourly_rate": 1500,
                "daily_rate": 12000,
                "project_rate_min": 20000,
                "project_rate_max": 80000,
                "availability_status": "available",
                "rating": 4.6,
                "total_projects": 32,
                "success_rate": 0.92,
                "skill_ids": [created_skills["UI/UX Design"], created_skills["Graphic Design"]]
            },
            {
                "name": "Rahul Kumar",
                "email": "rahul@example.com",
                "location": "Delhi",
                "bio": "Travel and landscape photographer with expertise in outdoor photography",
                "experience_years": 7,
                "hourly_rate": 2500,
                "daily_rate": 20000,
                "project_rate_min": 30000,
                "project_rate_max": 150000,
                "availability_status": "available",
                "rating": 4.9,
                "total_projects": 67,
                "success_rate": 0.97,
                "skill_ids": [created_skills["Landscape Photography"], created_skills["Street Photography"]]
            },
            {
                "name": "Sneha Patel",
                "email": "sneha@example.com",
                "location": "Pune",
                "bio": "Brand identity designer and illustrator",
                "experience_years": 4,
                "hourly_rate": 1800,
                "daily_rate": 14000,
                "project_rate_min": 25000,
                "project_rate_max": 90000,
                "availability_status": "available",
                "rating": 4.7,
                "total_projects": 38,
                "success_rate": 0.94,
                "skill_ids": [created_skills["Brand Identity"], created_skills["Illustration"]]
            },
            {
                "name": "Vikram Singh",
                "email": "vikram@example.com",
                "location": "Goa",
                "bio": "Wedding photographer and videographer",
                "experience_years": 6,
                "hourly_rate": 3000,
                "daily_rate": 25000,
                "project_rate_min": 50000,
                "project_rate_max": 200000,
                "availability_status": "available",
                "rating": 4.8,
                "total_projects": 89,
                "success_rate": 0.96,
                "skill_ids": [created_skills["Wedding Photography"], created_skills["Cinematography"]]
            },
            {
                "name": "Ananya Gupta",
                "email": "ananya@example.com",
                "location": "Mumbai",
                "bio": "Product photographer specializing in e-commerce",
                "experience_years": 3,
                "hourly_rate": 1800,
                "daily_rate": 14000,
                "project_rate_min": 20000,
                "project_rate_max": 70000,
                "availability_status": "available",
                "rating": 4.5,
                "total_projects": 56,
                "success_rate": 0.91,
                "skill_ids": [created_skills["Product Photography"], created_skills["Graphic Design"]]
            },
            {
                "name": "Rohan Desai",
                "email": "rohan@example.com",
                "location": "Bangalore",
                "bio": "Video editor and motion graphics artist",
                "experience_years": 4,
                "hourly_rate": 2200,
                "daily_rate": 18000,
                "project_rate_min": 30000,
                "project_rate_max": 120000,
                "availability_status": "busy",
                "rating": 4.6,
                "total_projects": 42,
                "success_rate": 0.93,
                "skill_ids": [created_skills["Video Editing"], created_skills["Motion Graphics"]]
            },
            {
                "name": "Kavya Nair",
                "email": "kavya@example.com",
                "location": "Delhi",
                "bio": "Content writer and social media strategist",
                "experience_years": 2,
                "hourly_rate": 1200,
                "daily_rate": 9000,
                "project_rate_min": 15000,
                "project_rate_max": 50000,
                "availability_status": "available",
                "rating": 4.4,
                "total_projects": 28,
                "success_rate": 0.89,
                "skill_ids": [created_skills["Content Writing"], created_skills["Social Media Marketing"]]
            }
        ]
        
        created_talents = {}
        for talent_data in talents_data:
            talent_obj = talent.create(db, TalentCreate(**talent_data))
            created_talents[talent_data["name"]] = talent_obj.id
            print(f"Created talent: {talent_data['name']}")
        
        # Create portfolio items
        portfolio_items = [
            {
                "talent_name": "Arjun Sharma",
                "items": [
                    {
                        "title": "Fashion Brand Campaign",
                        "description": "Complete fashion photography campaign for luxury brand",
                        "media_type": "image",
                        "project_type": "photography",
                        "client_name": "Luxury Fashion Brand",
                        "tags": "fashion, luxury, brand, campaign",
                        "style_keywords": "elegant, sophisticated, high-end"
                    },
                    {
                        "title": "Portrait Series",
                        "description": "Professional portrait series for corporate clients",
                        "media_type": "image",
                        "project_type": "photography",
                        "client_name": "Corporate Inc.",
                        "tags": "portrait, corporate, professional",
                        "style_keywords": "professional, clean, corporate"
                    }
                ]
            },
            {
                "talent_name": "Priya Mehta",
                "items": [
                    {
                        "title": "Mobile App UI Design",
                        "description": "Complete UI/UX design for food delivery app",
                        "media_type": "image",
                        "project_type": "design",
                        "client_name": "FoodTech Startup",
                        "tags": "ui, ux, mobile, app, food",
                        "style_keywords": "modern, intuitive, colorful"
                    }
                ]
            },
            {
                "talent_name": "Vikram Singh",
                "items": [
                    {
                        "title": "Destination Wedding",
                        "description": "Complete wedding photography and videography in Goa",
                        "media_type": "video",
                        "project_type": "photography",
                        "client_name": "Wedding Couple",
                        "tags": "wedding, destination, goa, celebration",
                        "style_keywords": "romantic, candid, tropical, vibrant"
                    }
                ]
            }
        ]
        
        for portfolio_data in portfolio_items:
            talent_id = created_talents[portfolio_data["talent_name"]]
            for item in portfolio_data["items"]:
                item_obj = portfolio_item.create(db, PortfolioItemCreate(**item), talent_id)
                print(f"Created portfolio item: {item['title']} for {portfolio_data['talent_name']}")
        
        # Create gigs
        gigs_data = [
            {
                "client_id": created_clients["TechStart Inc."],
                "title": "Product Photography for Tech Startup",
                "description": "We need professional product photography for our new tech gadgets. Clean, modern style with white background.",
                "category": "photography",
                "location": "Bangalore",
                "is_remote": False,
                "budget_min": 25000,
                "budget_max": 50000,
                "duration_days": 2,
                "start_date": datetime.now() + timedelta(days=7),
                "end_date": datetime.now() + timedelta(days=9),
                "style_preferences": "clean, modern, minimalist, white background",
                "deliverables": "50 edited product photos, different angles and lighting",
                "experience_required": "mid",
                "priority": "high",
                "required_skill_ids": [created_skills["Product Photography"]]
            },
            {
                "client_id": created_clients["Fashion Forward"],
                "title": "Fashion Brand Campaign Photographer",
                "description": "Looking for a talented fashion photographer for our sustainable fashion brand campaign. Need someone who can capture the essence of eco-friendly fashion.",
                "category": "photography",
                "location": "Mumbai",
                "is_remote": False,
                "budget_min": 75000,
                "budget_max": 150000,
                "duration_days": 3,
                "start_date": datetime.now() + timedelta(days=14),
                "end_date": datetime.now() + timedelta(days=16),
                "style_preferences": "natural, sustainable, eco-friendly, outdoor",
                "deliverables": "100 edited photos, behind-the-scenes content",
                "experience_required": "senior",
                "priority": "high",
                "required_skill_ids": [created_skills["Fashion Photography"]]
            },
            {
                "client_id": created_clients["Green Earth Co."],
                "title": "Brand Identity Design",
                "description": "We need a complete brand identity design for our sustainability consulting firm. Logo, business cards, letterhead, and brand guidelines.",
                "category": "design",
                "location": "Delhi",
                "is_remote": True,
                "budget_min": 40000,
                "budget_max": 80000,
                "duration_days": 10,
                "start_date": datetime.now() + timedelta(days=5),
                "end_date": datetime.now() + timedelta(days=15),
                "style_preferences": "eco-friendly, green, sustainable, professional",
                "deliverables": "Logo design, brand guidelines, business collateral",
                "experience_required": "mid",
                "priority": "medium",
                "required_skill_ids": [created_skills["Brand Identity"], created_skills["Graphic Design"]]
            },
            {
                "client_id": created_clients["Wedding Planners"],
                "title": "Travel Photography in Goa",
                "description": "I need a travel photographer in Goa for 3 days in November for a sustainable fashion brand. I want pastel tones and candid portraits. ₹75k max.",
                "category": "photography",
                "location": "Goa",
                "is_remote": False,
                "budget_min": 50000,
                "budget_max": 75000,
                "duration_days": 3,
                "start_date": datetime.now() + timedelta(days=30),
                "end_date": datetime.now() + timedelta(days=32),
                "style_preferences": "pastel tones, candid portraits, natural lighting",
                "deliverables": "150 edited photos, social media content",
                "experience_required": "mid",
                "priority": "high",
                "required_skill_ids": [created_skills["Portrait Photography"], created_skills["Fashion Photography"]]
            },
            {
                "client_id": created_clients["Creative Agency"],
                "title": "Social Media Content Creation",
                "description": "Looking for a content creator to develop social media strategy and create engaging content for our client's brand.",
                "category": "marketing",
                "location": "Pune",
                "is_remote": True,
                "budget_min": 30000,
                "budget_max": 60000,
                "duration_days": 15,
                "start_date": datetime.now() + timedelta(days=10),
                "end_date": datetime.now() + timedelta(days=25),
                "style_preferences": "engaging, creative, brand-focused",
                "deliverables": "Social media strategy, 30 posts, content calendar",
                "experience_required": "junior",
                "priority": "medium",
                "required_skill_ids": [created_skills["Social Media Marketing"], created_skills["Content Writing"]]
            }
        ]
        
        for gig_data in gigs_data:
            gig_obj = gig.create(db, GigCreate(**gig_data))
            print(f"Created gig: {gig_data['title']}")
        
        print(f"\nSample data created successfully!")
        print(f"Created {len(skills_data)} skills")
        print(f"Created {len(clients_data)} clients")
        print(f"Created {len(talents_data)} talents")
        print(f"Created {len(gigs_data)} gigs")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
