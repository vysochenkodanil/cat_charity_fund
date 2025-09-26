from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.charity_project import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)


class CharityProjectCRUD:
    async def get_multi(self, session: AsyncSession):
        result = await session.execute(select(CharityProject))
        return result.scalars().all()

    async def get_by_id(self, project_id: int, session: AsyncSession):
        result = await session.execute(
            select(CharityProject).where(CharityProject.id == project_id)
        )
        return result.scalars().first()

    async def get_by_name(self, name: str, session: AsyncSession):
        result = await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
        return result.scalars().first()

    async def create(
        self, obj_in: CharityProjectCreate, session: AsyncSession
    ) -> CharityProject:
        new_project = CharityProject(**obj_in.dict())
        session.add(new_project)
        await session.flush()
        await session.refresh(new_project)
        return new_project

    async def update(
        self,
        db_obj: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession,
    ) -> CharityProject:
        obj_data = obj_in.dict(exclude_unset=True)

        for field, value in obj_data.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj: CharityProject, session: AsyncSession):
        await session.delete(db_obj)
        await session.flush()
        return db_obj


charity_project_crud = CharityProjectCRUD()
