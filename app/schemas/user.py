from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass
