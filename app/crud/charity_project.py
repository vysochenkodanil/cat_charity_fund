from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from fastapi import HTTPException
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate


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
        await session.commit()
        await session.refresh(new_project)
        return new_project
    

    async def update(
        self,
        db_obj: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession
    ) -> CharityProject:
        if obj_in.full_amount and obj_in.full_amount < db_obj.invested_amount:
            raise HTTPException(
                status_code=400,
                detail="Нельзя уменьшить требуемую сумму меньше уже вложенной."
            )
        return await super().update(db_obj, obj_in, session)


    async def remove(self, db_obj: CharityProject, session: AsyncSession):
        await session.delete(db_obj)
        await session.commit()
        return db_obj


charity_project_crud = CharityProjectCRUD()
