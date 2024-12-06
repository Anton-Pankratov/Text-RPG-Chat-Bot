from typing import Type, List

from src.properties import T


async def map_db_rows(model_class: Type[T], rows: List[tuple], field_order: List[str]) -> List[T]:
    return [
        model_class(**dict(zip(field_order, row)))
        for row in rows
    ]