# Math Agent API — FastAPI Backend

FastAPI backend for the Quadratics skill mastery platform.

## Architecture

```
FastAPI (main.py)
├── /auth        → Supabase JWT verification
├── /skills      → List skills from Neo4j
├── /next-item   → Generate adaptive items (calls Python engine)
├── /grade       → Grade responses & update mastery (calls Python engine)
└── /progress    → Dashboard data (queries Neo4j)
```

## Getting Started

### 1. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Variables

Create `.env`:

```env
# Neo4j
NEO4J_URI=neo4j+s://your-aura-instance.neo4jlabs.io:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Supabase (optional, for production auth)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key

# Sentry (optional, for error tracking)
SENTRY_DSN=https://key@sentry.io/project

# Environment
ENVIRONMENT=development
```

### 3. Run Locally

```bash
# Development (auto-reload)
uvicorn app.main:app --reload

# Production
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

API will be at: `http://localhost:8000`

Swagger docs: `http://localhost:8000/docs`

## API Endpoints

See `/openapi.yaml` for full OpenAPI spec.

### Core Endpoints

- `GET /healthz` — Health check
- `POST /api/auth/session` — Verify auth token
- `GET /api/skills?domain=Quadratics` — List skills
- `POST /api/next-item` — Generate next item
- `POST /api/grade` — Grade response & update mastery
- `GET /api/progress?user_id=...` — Dashboard data

## Integration with Python Engine

The FastAPI routes call your existing Python engine functions:

```python
# In production routers, replace mock data with:
from engine.planner import generate_adaptive_item
from engine.state import update_after_answer
from engine.templates import grade

# Example: /api/next-item
async def next_item(req: NextItemRequest):
    item_dict = generate_adaptive_item(
        user_id=req.user_id,
        domain=req.domain,
        seed=req.seed
    )
    return NextItemResponse(...)
```

## Rate Limiting

Default limits:
- `/next-item`: 10 requests/min per IP
- `/grade`: 10 requests/min per IP

Override in `app/main.py`.

## Deployment

### Fly.io

```bash
flyctl launch
flyctl secrets set NEO4J_URI=... NEO4J_USER=... NEO4J_PASSWORD=...
flyctl deploy
```

### Render

1. Create new Web Service
2. Connect GitHub repo
3. Build command: `pip install -r api/requirements.txt`
4. Start command: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.app.main:app`
5. Add environment secrets

## Testing

```bash
pytest tests/
```

## Next Steps

1. **Integrate Python engine**: Replace mock data in routers with real calls
2. **Connect Neo4j**: Update routers to query skill graph and learner state
3. **Add Supabase auth**: Replace JWT mock with actual Supabase verification
4. **Rate limiting**: Configure per-route limits based on production needs
5. **Sentry integration**: Enable error tracking in production
