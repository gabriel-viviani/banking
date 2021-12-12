from pydantic import BaseModel
from datetime import date


class PersonSchema(BaseModel):
    name: str
    cpf: str
    birth_date: date
