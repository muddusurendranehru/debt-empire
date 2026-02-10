"""
Authentication routes: signup, login, logout
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.models import User
from auth import hash_password, verify_password, create_access_token
from middleware import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    phone: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SignUpResponse(BaseModel):
    message: str
    user_id: str
    email: str
    token: str


class LoginResponse(BaseModel):
    message: str
    user_id: str
    email: str
    token: str


@router.post("/signup", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignUpRequest):
    """
    User signup endpoint.
    Requires: email, password, confirm_password
    Optional: phone
    """
    # Validate passwords match
    if request.password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    # Validate password length
    if len(request.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters"
        )
    
    # Check if user already exists
    existing_user = User.get_by_email(request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    password_hash = hash_password(request.password)
    
    # Create user
    try:
        user = User.create(
            email=request.email,
            password_hash=password_hash,
            phone=request.phone
        )
        
        # Generate token
        token = create_access_token(user['id'], user['email'])
        
        return SignUpResponse(
            message="User created successfully",
            user_id=user['id'],
            email=user['email'],
            token=token
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    User login endpoint.
    Requires: email, password
    Returns: JWT token
    """
    # Get user by email
    user = User.get_by_email(request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(request.password, user['password_hash']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate token
    token = create_access_token(user['id'], user['email'])
    
    return LoginResponse(
        message="Login successful",
        user_id=user['id'],
        email=user['email'],
        token=token
    )


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user info."""
    return {
        "user_id": current_user['id'],
        "email": current_user['email'],
        "phone": current_user.get('phone')
    }


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout endpoint.
    Note: JWT tokens are stateless, so we just return success.
    Client should delete the token.
    """
    return {"message": "Logged out successfully"}
