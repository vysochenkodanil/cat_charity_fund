from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from app.api.routers import api_router
from app.core.config import settings
from app.core.user import auth_backend, get_user_manager
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

app = FastAPI(title=settings.app_title)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserCreate),
    prefix="/users",
    tags=["users"],
)


app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Welcome to QRKot API!"}
