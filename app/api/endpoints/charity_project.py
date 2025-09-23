from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB,
)
from app.services.investment import invest_donations

router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_project(
    project_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создать новый проект (только суперюзер)."""
    existing_project = await charity_project_crud.get_by_name(project_in.name, session)
    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проект с таким именем уже существует.",
        )

    new_project = await charity_project_crud.create(project_in, session)
    await invest_donations(new_project, session)
    return new_project


@router.get("/", response_model=list[CharityProjectDB])
async def get_all_projects(session: AsyncSession = Depends(get_async_session)):
    """Получить список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновить проект (только суперюзер)."""
    db_obj = await charity_project_crud.get_by_id(project_id, session)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Проект не найден")
    if db_obj.fully_invested:
        raise HTTPException(status_code=400, detail="Закрытые проекты нельзя редактировать")

    return await charity_project_crud.update(db_obj, obj_in, session)


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить проект (только суперюзер, если нет инвестиций)."""
    db_obj = await charity_project_crud.get_by_id(project_id, session)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Проект не найден")
    if db_obj.invested_amount > 0:
        raise HTTPException(status_code=400, detail="Нельзя удалить проект с пожертвованиями")

    return await charity_project_crud.remove(db_obj, session)
