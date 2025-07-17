# Talent Matchmaking Engine

A comprehensive backend API for matching creative talents with client projects, built with FastAPI and advanced matching algorithms.

## 🚀 Features

- **Advanced Matching Algorithm**: Rule-based and AI-powered talent matching
- **Comprehensive Talent Management**: Full CRUD operations for talent profiles
- **Client & Gig Management**: Handle client accounts and project requirements
- **Portfolio Management**: Support for talent portfolios and work samples
- **Feedback System**: Collect and analyze match feedback for continuous improvement
- **Real-time Analytics**: Dashboard statistics and performance metrics
- **RESTful API**: Well-documented API with interactive Swagger documentation
- **Database Support**: SQLAlchemy ORM with SQLite (easily configurable for PostgreSQL)

## 🏗️ Architecture

The system uses a sophisticated scoring algorithm that considers multiple factors:

- **Location compatibility** (20% weight)
- **Budget alignment** (25% weight)
- **Skills matching** (30% weight)
- **Experience level** (15% weight)
- **Availability status** (10% weight)
- **Portfolio relevance** (15% weight)
- **Talent rating** (10% weight)

## 📦 Installation

### Prerequisites

- Python 3.8+
- Git

### Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd talent-matchmaking-engine
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the application**:
```bash
uvicorn app.main:app --reload
```

6. **Populate sample data** (optional):
```bash
python scripts/populate_sample_data.py
```

## 🌐 API Documentation

Once the application is running, you can access:

- **Interactive API Documentation**: http://localhost:8000/docs
- **Alternative API Documentation**: http://localhost:8000/redoc
- **API Information**: http://localhost:8000/info

## 📚 API Endpoints

### Authentication & Health

- `GET /` - Root endpoint (redirects to docs)
- `GET /info` - Get API information
- `GET /api/v1/analytics/health` - Health check

### Clients

- `POST /api/v1/clients/` - Create a new client
- `GET /api/v1/clients/` - Get all clients
- `GET /api/v1/clients/{client_id}` - Get client by ID
- `PUT /api/v1/clients/{client_id}` - Update client
- `DELETE /api/v1/clients/{client_id}` - Delete client

### Talents

- `POST /api/v1/talents/` - Create a new talent
- `GET /api/v1/talents/` - Get all talents
- `GET /api/v1/talents/{talent_id}` - Get talent by ID
- `PUT /api/v1/talents/{talent_id}` - Update talent
- `DELETE /api/v1/talents/{talent_id}` - Delete talent
- `POST /api/v1/talents/search` - Search talents with filters
- `POST /api/v1/talents/{talent_id}/portfolio` - Add portfolio item
- `GET /api/v1/talents/{talent_id}/portfolio` - Get talent portfolio
- `DELETE /api/v1/talents/portfolio/{portfolio_item_id}` - Delete portfolio item

### Skills

- `POST /api/v1/skills/` - Create a new skill
- `GET /api/v1/skills/` - Get all skills
- `GET /api/v1/skills/{skill_id}` - Get skill by ID
- `GET /api/v1/skills/categories/list` - Get skill categories

### Gigs

- `POST /api/v1/gigs/` - Create a new gig
- `GET /api/v1/gigs/` - Get all gigs
- `GET /api/v1/gigs/{gig_id}` - Get gig by ID
- `PUT /api/v1/gigs/{gig_id}` - Update gig
- `DELETE /api/v1/gigs/{gig_id}` - Delete gig
- `POST /api/v1/gigs/search` - Search gigs with filters

### Matching

- `POST /api/v1/matching/find-matches` - Find talent matches for a gig
- `GET /api/v1/matching/gig/{gig_id}/matches` - Get existing matches for a gig
- `GET /api/v1/matching/talent/{talent_id}/matches` - Get matches for a talent
- `POST /api/v1/matching/rematch/{gig_id}` - Trigger rematch for a gig

### Feedback

- `POST /api/v1/matching/feedback` - Submit feedback on a match
- `GET /api/v1/matching/feedback/gig/{gig_id}` - Get feedback for a gig
- `GET /api/v1/matching/feedback/talent/{talent_id}` - Get feedback for a talent
- `GET /api/v1/matching/feedback/client/{client_id}` - Get feedback by client

### Analytics

- `GET /api/v1/analytics/dashboard` - Get dashboard statistics

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
DATABASE_URL=sqlite:///./talent_matchmaking.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your-openai-api-key-here
ENVIRONMENT=development
```

### Database Configuration

By default, the application uses SQLite. To use PostgreSQL:

1. Install PostgreSQL and create a database
2. Update `DATABASE_URL` in your `.env` file:
```env
DATABASE_URL=postgresql://username:password@localhost/talent_matchmaking
```

## 🤖 AI Features

The system supports AI-enhanced matching using sentence transformers:

### Enabling AI Matching

1. Install additional dependencies (included in requirements.txt):
```bash
pip install sentence-transformers scikit-learn
```

2. Use the AI matching endpoint:
```json
{
  "gig_id": "gig-id",
  "use_ai": true,
  "limit": 10
}
```

### AI Capabilities

- **Semantic Matching**: Matches project descriptions with portfolio items
- **Style Similarity**: Compares style preferences with past work
- **Enhanced Scoring**: Improves matching accuracy through embeddings

## 📊 Sample Data

The project includes a sample data script to populate the database with realistic test data:

```bash
python scripts/populate_sample_data.py
```

This creates:
- 18 skills across different categories
- 5 sample clients
- 8 sample talents with portfolios
- 5 sample gigs

## 🧪 Testing the API

### Example: Finding Matches for a Gig

1. **Create a client**:
```bash
curl -X POST "http://localhost:8000/api/v1/clients/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Client",
    "email": "test@example.com",
    "company": "Test Company",
    "location": "Mumbai"
  }'
```

2. **Create a gig**:
```bash
curl -X POST "http://localhost:8000/api/v1/gigs/" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "client-id",
    "title": "Fashion Photography",
    "description": "Need a fashion photographer for brand campaign",
    "category": "photography",
    "location": "Mumbai",
    "budget_min": 50000,
    "budget_max": 100000,
    "required_skill_ids": ["skill-id"]
  }'
```

3. **Find matches**:
```bash
curl -X POST "http://localhost:8000/api/v1/matching/find-matches" \
  -H "Content-Type: application/json" \
  -d '{
    "gig_id": "gig-id",
    "use_ai": false,
    "limit": 5
  }'
```

## 🔄 Matching Algorithm Details

### Rule-Based Matching

The core matching algorithm evaluates talents based on:

1. **Location Score**: Exact match (10), same region (7), same country (4)
2. **Budget Score**: Within 20% (10), 40% (7), 60% (4)
3. **Skills Score**: Exact skill match + category bonus
4. **Experience Score**: Perfect level match (10), overqualified (7)
5. **Availability Score**: Available (10), busy (3), unavailable (0)
6. **Portfolio Score**: Project type + style keywords + tags matching
7. **Rating Score**: Talent rating scaled to 10-point system

### AI-Enhanced Matching

When enabled, the system additionally considers:

- **Semantic Similarity**: Using sentence transformers to match descriptions
- **Style Matching**: Comparing style preferences with portfolio keywords
- **Context Understanding**: Better interpretation of project requirements

## 📈 Analytics & Monitoring

The system provides comprehensive analytics:

- **Dashboard Statistics**: Total counts, averages, trends
- **Match Performance**: Success rates, processing times
- **Talent Metrics**: Ratings, project completion rates
- **Client Insights**: Hiring patterns, feedback analysis

## 🔒 Security Features

- **Input Validation**: Pydantic models for request/response validation
- **Error Handling**: Comprehensive error responses
- **CORS Configuration**: Configurable cross-origin resource sharing
- **Environment-based Configuration**: Separate configs for development/production

## 🚀 Deployment

### Local Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment

1. **Set environment variables**:
```bash
export DATABASE_URL=postgresql://user:pass@localhost/db
export SECRET_KEY=your-production-secret
export ENVIRONMENT=production
```

2. **Run with Gunicorn**:
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

3. **Docker Deployment** (optional):
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:

1. Check the API documentation at `/docs`
2. Review the sample data script for examples
3. Check the logs for error details
4. Open an issue on GitHub

## 🎯 Future Enhancements

- [ ] Authentication and authorization
- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Integration with external services
- [ ] Machine learning model training
- [ ] Mobile app support
- [ ] Multi-language support

---

**Built with ❤️ for the creative community**
