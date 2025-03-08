from fastapi import APIRouter, Depends
from expiring_jwts.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/me")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": "Welcome to the protected route!", "user": user}
