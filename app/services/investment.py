from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invest_funds(session: AsyncSession):
    """Распределить средства между всеми проектами и донатами."""
    try:
        projects = await session.execute(
            select(CharityProject)
            .where(~CharityProject.fully_invested)
            .order_by(CharityProject.create_date)
        )
        projects = projects.scalars().all()

        donations = await session.execute(
            select(Donation)
            .where(~Donation.fully_invested)
            .order_by(Donation.create_date)
        )
        donations = donations.scalars().all()

        for donation in donations:
            await _process_donation(donation, projects, session)

        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise


async def invest_donation(donation: Donation, session: AsyncSession):
    """Распределить средства для конкретного пожертвования."""
    try:
        projects = await session.execute(
            select(CharityProject)
            .where(~CharityProject.fully_invested)
            .order_by(CharityProject.create_date)
        )
        projects = projects.scalars().all()

        await _process_donation(donation, projects, session)

        await session.commit()
        return donation
    except SQLAlchemyError:
        await session.rollback()
        raise


async def invest_project(project: CharityProject, session: AsyncSession):
    """Распределить средства в конкретный проект."""
    try:
        donations = await session.execute(
            select(Donation)
            .where(~Donation.fully_invested)
            .order_by(Donation.create_date)
        )
        donations = donations.scalars().all()

        for donation in donations:
            await _process_donation(donation, [project], session)

        await session.commit()
        return project
    except SQLAlchemyError:
        await session.rollback()
        raise


async def _process_donation(
    donation: Donation,
    projects: list[CharityProject],
    session: AsyncSession,
):
    """Распределить один донат по списку проектов."""
    remaining_donation = donation.full_amount - donation.invested_amount
    if remaining_donation <= 0:
        return

    for project in projects:
        if project.fully_invested or remaining_donation <= 0:
            continue

        needed = project.full_amount - project.invested_amount
        investment = min(needed, remaining_donation)

        project.invested_amount += investment
        donation.invested_amount += investment
        remaining_donation -= investment

        if project.invested_amount >= project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.utcnow()

        if donation.invested_amount >= donation.full_amount:
            donation.fully_invested = True
            donation.close_date = datetime.utcnow()

        session.add(project)
        session.add(donation)

        if remaining_donation <= 0:
            break
