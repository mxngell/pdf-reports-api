from pydantic import BaseModel, Field

class TableData(BaseModel):
    table_head: list[str] = Field(
        ...,
        description="Table header",
        examples=[["Месяц", "Продажи", "Выручка (руб.)"]]
    )
    table_rows: list[list[str]] = Field(
        ...,
        description="Table rows",
        examples=[["Январь", "115", "250.000"], ["Февраль", "88", "111.150"]]
    )