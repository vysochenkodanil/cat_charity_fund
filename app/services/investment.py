from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.charity_project import CharityProject
from app.models.donation import Donation

def _invest(obj_from, obj_to):
    """Распределяет средства между проектом и донатом."""
    amount_available = obj_from.full_amount - obj_from.invested_amount
    amount_needed = obj_to.full_amount - obj_to.invested_amount
    amount = min(amount_available, amount_needed)

    obj_from.invested_amount += amount
    obj_to.invested_amount += amount

    if obj_from.invested_amount == obj_from.full_amount:
        obj_from.fully_invested = True
        obj_from.close_date = datetime.utcnow()
    if obj_to.invested_amount == obj_to.full_amount:
        obj_to.fully_invested = True
        obj_to.close_date = datetime.utcnow()

    return amount


async def investment_process(
    new_project: CharityProject,
    session: AsyncSession
) -> CharityProject:
    """
    Универсальная функция для распределения средств между проектами и донатами.
    Вызывается после создания нового проекта или пожертвования.
    """
    # Получаем все открытые проекты, отсортированные по дате создания
    projects_result = await session.execute(
        select(CharityProject)
        .where(CharityProject.fully_invested == False)
        .order_by(CharityProject.create_date)
    )
    projects = projects_result.scalars().all()
    
    # Получаем все незакрытые пожертвования, отсортированные по дате создания
    donations_result = await session.execute(
        select(Donation)
        .where(Donation.fully_invested == False)
        .order_by(Donation.create_date)
    )
    donations = donations_result.scalars().all()
    
    if not projects or not donations:
        return
    
    # Распределяем пожертвования по проектам
    for project in projects:
        if project.fully_invested:
            continue
            
        for donation in donations:
            if donation.fully_invested:
                continue
                
            # Вычисляем оставшуюся сумму для проекта
            remaining_project = project.full_amount - project.invested_amount
            
            # Вычисляем оставшуюся сумму в пожертвовании
            remaining_donation = donation.full_amount - donation.invested_amount
            
            if remaining_project <= 0:
                break
                
            # Определяем сумму для инвестирования
            investment_amount = min(remaining_project, remaining_donation)
            
            # Обновляем суммы
            project.invested_amount += investment_amount
            donation.invested_amount += investment_amount
            
            # Проверяем, полностью ли заполнен проект
            if project.invested_amount >= project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.utcnow()
            
            # Проверяем, полностью ли распределено пожертвование
            if donation.invested_amount >= donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.utcnow()
                
            if project.fully_invested:
                break
    
    await session.commit()


# Алиасы для обратной совместимости
invest_to_projects = investment_process