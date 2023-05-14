from fastapi_sa_orm_filter.main import FilterCore
from sqlalchemy import func
from sqlalchemy.sql.expression import or_, select


class CustomFilter(FilterCore):
    def __init__(self, model, allowed_filters):
        super().__init__(model, allowed_filters)

    def get_unordered_query(self, conditions):
        unordered_query = select(
            self._model.id,
            self._model.title,
            func.sum(self._model.salary_from).label("salary_from"),
            self._model.is_active
        ).filter(or_(*conditions)).group_by(self._model.is_active)
        return unordered_query
