from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession

from database import VacancyCategory, Vacancy


async def create_vacancies(session: AsyncSession):
    vacancy_instances = []
    enum_category = [member.name for member in VacancyCategory]
    for i in range(1, 11):
        vacancy = Vacancy(
            title=f"title{i}",
            description=f"description{i}",
            salary_from=50 + i * 10,
            salary_up_to=100.725 + i * 10,
            created_at=date(2023, 5, i),
            updated_at=datetime(2023, i, 5, 15, 15, 15),
            category=VacancyCategory[enum_category[i - 1]],
            is_active=bool(i % 2)
        )
        vacancy_instances.append(vacancy)
    session.add_all(vacancy_instances)
    await session.commit()
