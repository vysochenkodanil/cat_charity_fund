# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select

# from app.models.donation import Donation
# from app.schemas.donation import DonationCreate


# class DonationCRUD:
#     async def get_multi(self, session: AsyncSession):
#         result = await session.execute(select(Donation))
#         return result.scalars().all()

#     async def get_by_user(self, user_id: str, session: AsyncSession):
#         result = await session.execute(
#             select(Donation).where(Donation.user_id == user_id)
#         )
#         return result.scalars().all()

#     async def create(
#         self, obj_in: DonationCreate, user_id: str, session: AsyncSession
#     ) -> Donation:
#         new_donation = Donation(**obj_in.dict(), user_id=user_id)
#         session.add(new_donation)
#         await session.commit()
#         await session.refresh(new_donation)
#         return new_donation


# donation_crud = DonationCRUD()
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Donation
from app.schemas.donation import DonationCreate

async def create_donation(
    donation_in: DonationCreate,
    user_id: int,
    session: AsyncSession,
) -> Donation:
    donation_data = donation_in.dict()
    donation = Donation(**donation_data, user_id=user_id)
    session.add(donation)
    await session.commit()
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
