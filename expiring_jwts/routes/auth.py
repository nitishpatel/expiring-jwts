from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from expiring_jwts.core.db import get_db
from expiring_jwts.models.user import User
from expiring_jwts.schemas.auth_schema import UserCreate, UserOut, Token,UserLogin
from expiring_jwts.auth.hashing import hash_password, verify_password, create_access_token
from sqlalchemy.orm import Session
router = APIRouter()
from sqlalchemy.ext.asyncio import AsyncSession

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    '''
    Register a new user
    '''
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(username=user.username, email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    '''
    Login a user
    '''
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalars().first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
