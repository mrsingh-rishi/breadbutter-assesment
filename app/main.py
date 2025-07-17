from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.core.database import engine, Base
from app.api import clients, talents, skills, gigs, matching, analytics
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="""
    ## Talent Matchmaking Engine API

    A comprehensive API for matching creative talents with client projects.

    ### Features:
    - **Talent Management**: Create, update, and manage talent profiles
    - **Client Management**: Handle client accounts and project requirements
    - **Gig Management**: Create and manage project listings
    - **Advanced Matching**: Rule-based and AI-powered talent matching
    - **Portfolio Management**: Handle talent portfolios and work samples
    - **Feedback System**: Collect and analyze match feedback
    - **Analytics**: Comprehensive dashboard and statistics

    ### Matching Algorithm:
    The system uses a sophisticated scoring algorithm that considers:
    - **Location compatibility** (20% weight)
    - **Budget alignment** (25% weight)
    - **Skills matching** (30% weight)
    - **Experience level** (15% weight)
    - **Availability status** (10% weight)
    - **Portfolio relevance** (15% weight)
    - **Talent rating** (10% weight)

    ### AI Enhancement:
    When enabled, the system uses sentence transformers for semantic matching of:
    - Project descriptions with portfolio items
    - Style preferences with past work
    - Client requirements with talent capabilities
    """,
    contact={
        "name": "BreadButter Team",
        "url": "https://breadbutter.com",
        "email": "api@breadbutter.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    clients.router,
    prefix=f"{settings.api_v1_str}/clients",
    tags=["clients"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    talents.router,
    prefix=f"{settings.api_v1_str}/talents",
    tags=["talents"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    skills.router,
    prefix=f"{settings.api_v1_str}/skills",
    tags=["skills"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    gigs.router,
    prefix=f"{settings.api_v1_str}/gigs",
    tags=["gigs"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    matching.router,
    prefix=f"{settings.api_v1_str}/matching",
    tags=["matching"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    analytics.router,
    prefix=f"{settings.api_v1_str}/analytics",
    tags=["analytics"],
    responses={404: {"description": "Not found"}},
)


@app.get("/")
async def root():
    """Root endpoint redirects to API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/info")
async def info():
    """Get API information."""
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": "Advanced talent matchmaking engine for creative professionals",
        "environment": settings.environment,
        "features": [
            "Advanced matching algorithm",
            "AI-powered semantic matching",
            "Portfolio management",
            "Feedback collection",
            "Real-time analytics",
            "RESTful API"
        ],
        "matching_weights": {
            "location": "20%",
            "budget": "25%",
            "skills": "30%",
            "experience": "15%",
            "availability": "10%",
            "portfolio": "15%",
            "rating": "10%"
        }
    }


# Add startup event
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.project_name} v{settings.version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Database: {settings.database_url}")


# Add shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.project_name}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
