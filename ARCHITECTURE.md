# Math Agent — Production Website Architecture

## Overview

A monorepo containing a full-stack production-ready learning platform for Quadratics skill mastery.

```
Browser (Next.js)
    ↕ (HTTPS)
Frontend (web/)
    ↕ (REST API)
FastAPI Backend (api/)
    ↕
Neo4j Graph Database
    ↕
Supabase Auth + Storage
```

## Directory Structure

```
quadratics_web/
├── api/                    # FastAPI backend (Python)
│   ├── app/
│   │   ├── main.py        # FastAPI app + middleware
│   │   ├── routers/       # Endpoint implementations
│   │   │   ├── auth.py    # JWT verification
│   │   │   ├── skills.py  # List skills from Neo4j
│   │   │   ├── learning.py # next-item, grade endpoints
│   │   │   └── progress.py # Dashboard data
│   │   ├── models/        # Pydantic request/response models
│   │   └── services/      # Business logic (Neo4j, engine integration)
│   ├── requirements.txt
│   ├── openapi.yaml       # OpenAPI/Swagger spec
│   ├── Dockerfile         # For containerization
│   └── README.md
│
├── web/                    # Next.js frontend (TypeScript/React)
│   ├── app/               # App directory structure
│   │   ├── page.tsx       # Landing page
│   │   ├── app/           # Student learning interface
│   │   ├── dashboard/     # Teacher progress dashboard
│   │   ├── auth/          # Auth flows
│   │   └── layout.tsx     # Root layout
│   ├── components/        # Reusable components
│   │   ├── Question.tsx
│   │   ├── SkillCard.tsx
│   │   ├── ProgressBar.tsx
│   │   └── ...
│   ├── lib/              # Utilities
│   │   ├── api.ts        # API client (axios + auth)
│   │   ├── auth.ts       # Supabase auth helpers
│   │   └── types.ts      # Shared TypeScript types
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   └── README.md
│
├── shared/               # Shared types & schemas (optional)
│   ├── types.ts
│   └── constants.ts
│
├── .github/workflows/    # GitHub Actions CI/CD
│   ├── test.yml          # Run pytest on API
│   └── deploy.yml        # Deploy to Vercel + Fly.io
│
├── docker-compose.yml    # Local dev stack (optional)
├── openapi.yaml          # (symlink from api/)
├── ARCHITECTURE.md       # This file
└── README.md
```

## Technology Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (Radix UI + Tailwind)
- **Auth**: Supabase Auth SDK
- **HTTP Client**: axios
- **Build**: Vercel

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Web Server**: Uvicorn
- **Database**: Neo4j Aura
- **Auth Validation**: PyJWT
- **Rate Limiting**: slowapi
- **Error Tracking**: Sentry
- **Container**: Docker
- **Deployment**: Fly.io or Render

### Shared
- **Type Safety**: TypeScript (frontend) + Pydantic (backend)
- **API Contract**: OpenAPI 3.0 spec
- **Monitoring**: Sentry, health checks

## Data Flow

### 1. User Authentication
```
Student Login
    ↓
Next.js Auth Page (Supabase UI)
    ↓
Supabase Auth Provider
    ↓
JWT Access Token → Frontend localStorage
    ↓
Next: POST /api/auth/session with JWT
    ↓
FastAPI verifies signature
    ↓
UserSession → Frontend
```

### 2. Getting Next Question
```
Student clicks "Get Next Question"
    ↓
Frontend: POST /api/next-item { user_id, domain, seed? }
    ↓
FastAPI calls engine.generate_adaptive_item()
    ↓
Engine queries Neo4j for mastery, misconceptions, prerequisites
    ↓
Engine generates item based on mastery & planner logic
    ↓
Response: Item + reason + mastery_before
    ↓
Frontend renders question with 4 choices
```

### 3. Submitting Answer
```
Student selects answer + clicks Submit
    ↓
Frontend: POST /api/grade { user_id, item_id, choice_id, time_ms, confidence }
    ↓
FastAPI calls engine.grade()
    ↓
Engine validates answer against tags_on_select
    ↓
Engine updates mastery equation: p_mastery_after
    ↓
FastAPI writes to Neo4j:
  - CREATE Attempt node (immutable log)
  - UPDATE HAS_PROGRESS (mastery, attempts, streak)
  - MERGE HAS_ERROR (misconception counts)
    ↓
Response: { correct, tags, p_mastery_after, next_due_at, resource_url? }
    ↓
Frontend shows feedback + updates mastery bar
```

### 4. Viewing Progress (Dashboard)
```
Teacher navigates to /dashboard
    ↓
Frontend: GET /api/progress?user_id=...
    ↓
FastAPI queries Neo4j:
  - All HAS_PROGRESS edges
  - Recent Attempt nodes
  - HAS_ERROR counts per tag
    ↓
Response: ProgressResponse with skills, misconceptions, weekly stats, due_today
    ↓
Frontend renders skill cards, error heatmap, weekly chart
```

## API Contract

All endpoints documented in `openapi.yaml`.

### Authentication
- All endpoints (except `/healthz`) require `Authorization: Bearer <JWT>`
- JWT issued by Supabase
- Verified in `POST /api/auth/session` first

### Rate Limits
- `/api/next-item`: 10 req/min per IP (or per user_id in production)
- `/api/grade`: 10 req/min per IP

### Error Handling
- Standard JSON error responses with `error` code + `message`
- 4xx client errors, 5xx server errors (with Sentry logging)

## Development Workflow

### Local Setup
```bash
# 1. Clone & install
git clone https://github.com/sunnyzhengai/Math_Agent.git
cd quadratics_web

# 2. Backend
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Configure .env with NEO4J_URI, etc.
uvicorn app.main:app --reload

# 3. Frontend (new terminal)
cd web
npm install
npm run dev
```

### Making Changes
- **Backend**: Edit `api/app/routers/*.py`, routes auto-reload
- **Frontend**: Edit `web/app/**/*.tsx`, HMR auto-refreshes
- **API spec**: Update `api/openapi.yaml`, use for documentation

### Testing
```bash
# Backend
cd api
pytest tests/

# Frontend
cd web
npm test
```

## Deployment

### Staging
1. Push to `develop` branch
2. GitHub Actions runs pytest on API
3. Next.js deploys to Vercel preview
4. FastAPI deploys to Fly.io staging slot

### Production
1. Push to `main` branch (or create release tag)
2. GitHub Actions runs full test suite
3. Vercel auto-deploys frontend to mathagent.app
4. Fly.io auto-deploys backend API to api.mathagent.app
5. Health checks verify endpoints

### Environment Secrets
**Vercel (frontend)**
- `NEXT_PUBLIC_API_URL=https://api.mathagent.app`
- `NEXT_PUBLIC_SUPABASE_URL=...`
- `NEXT_PUBLIC_SUPABASE_KEY=...`

**Fly.io (backend)**
- `NEO4J_URI=neo4j+s://...`
- `NEO4J_USER=neo4j`
- `NEO4J_PASSWORD=...`
- `SUPABASE_URL=...`
- `SUPABASE_KEY=...`
- `SENTRY_DSN=...`

## Security Considerations

1. **Auth**: Supabase handles user authentication; backend validates JWT
2. **CORS**: Restricted to frontend domain (`https://mathagent.app`)
3. **Rate Limiting**: Prevents brute force / DoS
4. **HTTPS**: All production endpoints use TLS
5. **COPPA Compliance**: Parental consent checkbox on signup (Julia is minor)
6. **Data**: Only store attempts + skill IDs; pseudonymize user IDs with UUIDs

## Monitoring

### Sentry (Error Tracking)
- Captures FastAPI exceptions
- Captures Next.js JS errors
- Links to GitHub commits for quick debugging

### Health Checks
- `GET /healthz` → `{ status: "ok", timestamp }`
- Used by load balancers to verify service health

### Logging
- Backend: FastAPI request logs + Sentry
- Frontend: Sentry JS error logs
- Neo4j: Query logs for performance tuning

## Next Steps (Priority Order)

1. **Integrate Python engine**: Replace mock data in `/api/app/routers/learning.py`
2. **Connect Neo4j**: Update routers to query skill graph (from quadratics_mvp)
3. **Build Next.js frontend**: Landing page + auth + student app + dashboard
4. **Supabase auth**: Wire Supabase login to Next.js
5. **Deploy**: Set up Vercel + Fly.io with CI/CD
6. **Polish**: Loading states, error boundaries, accessibility
7. **Analytics**: Add tracking for user behavior
8. **Testing**: E2E tests with Playwright

---

**Version**: 1.0 | **Last Updated**: 2025-10-31
