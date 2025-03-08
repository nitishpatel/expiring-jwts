from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from expiring_jwts.auth.hashing import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Extracts the current user from the JWT token"""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload  # You can access user details inside protected routes
