import uuid
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str
