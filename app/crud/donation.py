from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.donation import Donation
from app.schemas.donation import DonationCreate


async def create_donation(
    donation_in: DonationCreate,
    user_id: int,
    session: AsyncSession,
) -> Donation:
    donation_data = donation_in.dict()
    donation = Donation(**donation_data, user_id=user_id)
    session.add(donation)
    await session.flush()  # Только flush, не commit
    await session.refresh(donation)
    return donation


async def get_by_user(
    user_id: int,
    session: AsyncSession,
) -> list[Donation]:
    donations = await session.execute(
        select(Donation).where(Donation.user_id == user_id)
    )
    return donations.scalars().all()


async def get_multi(
    session: AsyncSession,
) -> list[Donation]:
    donations = await session.execute(select(Donation))
    return donations.scalars().all()


class DonationCRUD:
    def __init__(self):
        self.create = create_donation
        self.get_by_user = get_by_user
        self.get_multi = get_multi


donation_crud = DonationCRUD()
