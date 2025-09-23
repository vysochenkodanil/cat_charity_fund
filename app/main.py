# from fastapi import FastAPI

# from app.core.db import Base, get_async_session
# from app.core.user import auth_backend, fastapi_users, current_user, current_superuser
# from app.api.routers import api_router

# app = FastAPI(title="QRKot")

# # Подключение роутеров FastAPI Users
# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth/jwt",
#     tags=["Auth"],
# )
# app.include_router(
#     fastapi_users.get_register_router(),
#     prefix="/auth",
#     tags=["Auth"],
# )
# app.include_router(
#     fastapi_users.get_users_router(),
#     prefix="/users",
#     tags=["Users"],
# )

# # Подключение наших роутеров
# app.include_router(api_router)
from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from app.api.routers import main_router
from app.core.config import settings
from app.core.user import auth_backend, get_user_manager, current_user, current_superuser
from app.models.user import User
from app.schemas.user import UserRead, UserCreate

app = FastAPI(title=settings.app_title)

# Настройка FastAPI Users
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Подключение роутеров аутентификации
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

# Подключение основных роутеров приложения
app.include_router(main_router)

@app.get("/")
async def root():
    return {"message": "Welcome to QRKot API!"}