from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sentry_sdk
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Import routers
from .routers import auth, skills, learning, progress

# Initialize Sentry for error tracking (optional)
def init_sentry():
    """Initialize Sentry error tracking."""
    sentry_dsn = None  # Load from env
    if sentry_dsn:
        sentry_sdk.init(dsn=sentry_dsn, traces_sample_rate=0.1)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    # Startup
    init_sentry()
    print("✅ Math Agent API started")
    yield
    # Shutdown
    print("👋 Math Agent API shutdown")

# Create FastAPI app
app = FastAPI(
    title="Math Agent API",
    description="Quadratics skill mastery platform backend",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://mathagent.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda r, e: {"error": "rate_limit_exceeded", "message": str(e)})

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(skills.router, prefix="/api/skills", tags=["skills"])
app.include_router(learning.router, prefix="/api", tags=["learning"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])

# Health check
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime

@app.get("/healthz", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok", timestamp=datetime.utcnow())

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Math Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
