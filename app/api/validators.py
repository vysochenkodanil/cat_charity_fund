from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def get_project_or_404(
    project_id: int, session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get_by_id(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Проект не найден."
        )
    return charity_project


async def check_name_duplicate(
    project_name: str, session: AsyncSession
) -> None:
    if await charity_project_crud.get_by_name(project_name, session):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует.",
        )


async def check_charity_project_before_delete(
    project_id: int, session: AsyncSession
) -> CharityProject:
    charity_project = await get_project_or_404(project_id, session)
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект уже внесены средства, его нельзя удалить.",
        )
    return charity_project


async def check_charity_project_before_edit(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await get_project_or_404(project_id, session)

    # Проверка что проект не закрыт
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )

    # Проверка что новая сумма не меньше уже инвестированной
    if obj_in.full_amount is not None:
        if obj_in.full_amount < charity_project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Новая сумма не может быть меньше уже внесенной.",
            )

    # Проверка на дубликат имени
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    return charity_project


# НОВЫЕ ВАЛИДАТОРЫ ДЛЯ ПРОХОЖДЕНИЯ ТЕСТОВ:


async def check_project_description_not_empty(description: str) -> None:
    """Проверка что описание не пустое."""
    if description is not None and description.strip() == "":
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Описание не может быть пустым.",
        )


async def check_no_system_fields_in_update(
    obj_in: CharityProjectUpdate,
) -> None:
    """Проверка что не обновляются системные поля."""
    forbidden_fields = [
        "invested_amount",
        "create_date",
        "close_date",
        "fully_invested",
    ]

    # Получаем только те поля, которые действительно переданы для обновления
    update_data = obj_in.dict(exclude_unset=True)

    for field in forbidden_fields:
        if field in update_data:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f"Запрещено изменять поле {field}.",
            )


async def validate_charity_project_create(
    name: str, description: str, full_amount: int, session: AsyncSession
) -> None:
    """Валидация при создании проекта."""
    # Проверка дубликата имени
    await check_name_duplicate(name, session)

    # Проверка что описание не пустое
    await check_project_description_not_empty(description)

    # Проверка что сумма положительная
    if full_amount <= 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Сумма проекта должна быть больше 0.",
        )


async def validate_charity_project_update(
    project_id: int, obj_in: CharityProjectUpdate, session: AsyncSession
) -> CharityProject:
    """Полная валидация при обновлении проекта."""
    # Проверка системных полей
    await check_no_system_fields_in_update(obj_in)

    # Проверка проекта и базовых условий
    project = await check_charity_project_before_edit(
        project_id, obj_in, session
    )

    # Проверка описания если оно передано
    if obj_in.description is not None:
        await check_project_description_not_empty(obj_in.description)

    return project
