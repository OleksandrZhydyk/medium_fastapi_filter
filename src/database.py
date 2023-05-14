from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, Date, Float, Enum as sa_enum
from enum import Enum

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker


class VacancyCategory(str, Enum):
    finance = "Finance"
    marketing = "Marketing"
    agro = "Agriculture"
    it = "IT"
    metallurgy = "Metallurgy"
    medicine = "Medicine"
    construction = "Construction"
    building = "Building"
    services = "Services"
    miscellaneous = "Miscellaneous"


DB_URL = 'sqlite+aiosqlite:///fastapi_sa_filter.db'

Base = declarative_base()


# SQLAlchemy database model
class Vacancy(Base):
    __tablename__ = "vacancies"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(Date)
    updated_at = Column(DateTime)
    salary_from = Column(Integer)
    salary_up_to = Column(Float)
    category = Column(sa_enum(VacancyCategory), nullable=False)


engine = create_async_engine(DB_URL, echo=True, future=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Create tables in the database
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Return database session object
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
