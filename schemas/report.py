from datetime import date
from typing import Annotated
from pydantic import BaseModel, Field
from pydantic_extra_types.phone_numbers import PhoneNumber, PhoneNumberValidator
import secrets

from schemas.table import TableData

PhoneNumberType = Annotated[
    str | PhoneNumber,
    PhoneNumberValidator(default_region="RU", number_format="E164")  
]

class ReportDataIn(BaseModel):
    title: str = Field(
        "Отёт",
        description="Report title",
        examples=["Официальное уведомление"]
    )
    recipient_name: str = Field(
        ..., 
        description="Recipient's name",
        examples=["А. А. Алексеевич"]
    )
    recipient_contact: PhoneNumberType = Field(
        ..., 
        description="Recipient's contact (E.164 format)",
        examples=["89817777777"]
    )
    sender_name: str = Field(
        ...,
        description="Sender's name",
        examples=["П. П. Петрович"]
    )
    sender_contact: PhoneNumberType = Field(
        ..., 
        description="Sender's contact (E.164 format)",
        examples=["89818888888"]
    )
    report_content: str = Field(
        "Текст отсутствует", 
        description="Report text",
        examples=["Значимость этих проблем настолько очевидна, что выбранный нами стратегический путь не совсем подходящий..."]
    )
    table: TableData = Field(
        ...,
        description="Table data",
        examples=[
            {
                "table_head": ["Месяц", "Продажи", "Выручка (руб.)"],
                "table_rows": [["Январь", "115", "250.000"], ["Февраль", "88", "111.150"]]
            }
        ]
    )
    city: str = Field(
        "Москва",
        description="City",
        examples=["Москва"]
    )

class ReportData(ReportDataIn):
    id: int = secrets.randbits(32)
    current_date: str = date.today().strftime("%d.%m.%Y")
    current_year: int = date.today().year