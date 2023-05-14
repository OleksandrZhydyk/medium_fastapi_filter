from datetime import date, datetime

from pydantic import BaseModel, constr, Field

from database import VacancyCategory

# Pydantic schema for validation and serialization of output data
class VacancyOut(BaseModel):
    id: int
    title: constr(min_length=1)
    description: constr(min_length=1)
    salary_from: int = Field(..., gt=0)
    salary_up_to: int = Field(..., gt=0)
    category: VacancyCategory
    is_active: bool
    created_at: date
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda date: date.isoformat()[:-3] + "Z"}


# Pydantic schema for validation and serialization of custom output data
class CustomVacancyOut(BaseModel):
    id: int
    title: constr(min_length=1)
    salary_from: int = Field(..., gt=0)
    is_active: bool

    class Config:
        orm_mode = True
