from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.donation import Donation
from app.schemas.donation import DonationCreate


class DonationCRUD:
    """CRUD-операции для модели Donation."""

    async def create(
        self,
        donation_in: DonationCreate,
        user_id: int,
        session: AsyncSession,
    ) -> Donation:
        """Создать пожертвование."""
        donation_data = donation_in.dict()
        donation = Donation(**donation_data, user_id=user_id)
        session.add(donation)
        await session.flush()
        await session.refresh(donation)
        return donation

    async def get_by_user(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> list[Donation]:
        """Получить все пожертвования конкретного пользователя."""
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        return donations.scalars().all()

    async def get_multi(
        self,
        session: AsyncSession,
    ) -> list[Donation]:
        """Получить все пожертвования."""
        donations = await session.execute(select(Donation))
        return donations.scalars().all()


donation_crud = DonationCRUD()
