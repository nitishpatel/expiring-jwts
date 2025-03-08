"""Main router file for the application.

This module contains the main router that includes all other routers for
the application.
"""

from fastapi import APIRouter

from expiring_jwts.routes.auth import router as auth_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
