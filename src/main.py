from typing import List
from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_sa_orm_filter.main import FilterCore
from fastapi_sa_orm_filter.operators import Operators as ops

from custom_select_query import CustomFilter
from database import init_models, get_session, Vacancy
from fake_data import create_vacancies
from schemas import VacancyOut, CustomVacancyOut

# Create FastAPI application
app = FastAPI(title="FastAPI_filter")


# Create tables in the database when the app starts
@app.on_event("startup")
async def startup():
    await init_models()


# Route for fake data creation
@app.get("/create_data")
async def get_filtered_vacancies(session: AsyncSession = Depends(get_session)):
    await create_vacancies(session=session)


# Define fields and operators for filter
my_objects_filter = {
    'title': [ops.eq, ops.in_, ops.like, ops.startswith, ops.contains],
    'is_active': [ops.eq],
    'created_at': [ops.between, ops.eq, ops.gt, ops.lt, ops.in_],
    'salary_from': [ops.between, ops.not_eq, ops.gte, ops.lte]
}


# Route for filter with default select expression (all table columns selected)
@app.get("/")
async def get_filtered_vacancies(
        objects_filter: str = Query(default=''),
        db: AsyncSession = Depends(get_session)
) -> List[VacancyOut]:

    filter_inst = FilterCore(Vacancy, my_objects_filter)
    query = filter_inst.get_query(objects_filter)
    db_obj = await db.execute(query)
    instance = db_obj.scalars().all()
    return instance


# Route for filter with custom select expression
@app.get("/custom_select")
async def get_filtered_vacancies(
        objects_filter: str = Query(default=''),
        db: AsyncSession = Depends(get_session)
) -> List[CustomVacancyOut]:

    filter_inst = CustomFilter(Vacancy, my_objects_filter)
    query = filter_inst.get_query(objects_filter)
    db_obj = await db.execute(query)
    instance = db_obj.all()
    return instance
