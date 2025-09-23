from fastapi import APIRouter

from app.api.endpoints import charity_project, donation

api_router = APIRouter()

api_router.include_router(
    charity_project.router,
    prefix="/charity_project",
    tags=["Charity Projects"],
)

api_router.include_router(
    donation.router,
    prefix="/donation",
    tags=["Donations"],
)
