from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
import jwt

router = APIRouter()

# Schemas
class SessionRequest(BaseModel):
    access_token: str

class UserSession(BaseModel):
    user_id: str
    email: str
    role: str  # student, teacher, admin
    authenticated_at: datetime

# Mock Supabase JWT verification
# In production, use: from supabase import create_client
def verify_supabase_token(token: str) -> dict:
    """
    Verify Supabase JWT token.
    In production, this should use the actual Supabase client.
    """
    try:
        # Decode token (in production, verify with Supabase public key)
        # For now, just validate structure
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "invalid_token", "message": str(e)}
        )

@router.post("/session", response_model=UserSession)
async def get_session(req: SessionRequest):
    """
    Verify auth token and return user session.
    Expects Supabase JWT access token.
    """
    payload = verify_supabase_token(req.access_token)
    
    # Extract user info from token payload
    user_id = payload.get("sub")  # Supabase user ID
    email = payload.get("email")
    
    if not user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "invalid_token", "message": "Missing required claims"}
        )
    
    # Determine role (default: student)
    # In production, query from database
    role = payload.get("role", "student")
    
    return UserSession(
        user_id=user_id,
        email=email,
        role=role,
        authenticated_at=datetime.utcnow()
    )
