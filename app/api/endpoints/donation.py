from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate, DonationDB, DonationUserDB
from app.services.investment import invest_donation

router = APIRouter()


@router.post(
    "/", response_model=DonationUserDB, response_model_exclude_none=True
)
async def create_donation(
    donation_in: DonationCreate,
    user=Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Сделать пожертвование (для авторизованных пользователей)."""
    new_donation = await donation_crud.create(donation_in, user.id, session)
    await invest_donation(new_donation, session)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get("/my", response_model=list[DonationUserDB])
async def get_my_donations(
    user=Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Посмотреть список своих пожертвований
    (только авторизованные пользователи)
    """
    return await donation_crud.get_by_user(user.id, session)


@router.get(
    "/",
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Посмотреть список всех пожертвований (только суперюзер)."""
    return await donation_crud.get_multi(session)
