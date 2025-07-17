#!/usr/bin/env python3
"""
Simple test script to verify the FastAPI application works correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work correctly."""
    try:
        from app.main import app
        print("✅ Main app imported successfully")
        
        from app.models.models import Client, Talent, Skill, Gig
        print("✅ Database models imported successfully")
        
        from app.services.matchmaking import rule_based_engine
        print("✅ Matchmaking engine imported successfully")
        
        from app.crud.crud import client, talent, skill, gig
        print("✅ CRUD operations imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality."""
    try:
        from app.core.database import SessionLocal
        from app.crud.crud import client, talent, skill, gig
        
        db = SessionLocal()
        
        # Test database connection
        talents = talent.get_multi(db, limit=5)
        print(f"✅ Database connected - found {len(talents)} talents")
        
        clients = client.get_multi(db, limit=5)
        print(f"✅ Found {len(clients)} clients")
        
        skills = skill.get_multi(db, limit=10)
        print(f"✅ Found {len(skills)} skills")
        
        gigs = gig.get_multi(db, limit=5)
        print(f"✅ Found {len(gigs)} gigs")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Functionality error: {e}")
        return False

def test_matching_algorithm():
    """Test the matching algorithm."""
    try:
        from app.core.database import SessionLocal
        from app.crud.crud import gig
        from app.services.matchmaking import rule_based_engine
        
        db = SessionLocal()
        
        # Get a sample gig
        gigs = gig.get_multi(db, limit=1)
        if gigs:
            sample_gig = gigs[0]
            print(f"✅ Testing matching for gig: {sample_gig.title}")
            
            # Test matching
            matches = rule_based_engine.find_matches(db, sample_gig.id, limit=3)
            print(f"✅ Found {len(matches)} matches")
            
            for match in matches:
                print(f"   - {match.talent.name}: {match.match_score:.2f}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Matching algorithm error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Talent Matchmaking Engine")
    print("=" * 50)
    
    success = True
    
    print("\n1. Testing imports...")
    success &= test_imports()
    
    print("\n2. Testing basic functionality...")
    success &= test_basic_functionality()
    
    print("\n3. Testing matching algorithm...")
    success &= test_matching_algorithm()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! The application is ready to use.")
        print("\nNext steps:")
        print("1. Run: python run.py")
        print("2. Or run: uvicorn app.main:app --reload")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
