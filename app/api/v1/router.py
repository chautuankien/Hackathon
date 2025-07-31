from fastapi import APIRouter
from app.api.v1 import auth

v1_router = APIRouter(prefix="/v1")

# Include all route modules
v1_router.include_router(auth.router)