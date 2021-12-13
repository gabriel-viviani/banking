from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal
from datetime import date
from enum import Enum
from uuid import UUID


class PersonSchema(BaseModel):
    name: str
    cpf: str
    birth_date: date


class AccountTypes(str, Enum):
    salary = "salary"
    savings = "savings"
    checking = "checking"


class Account(BaseModel):
    daily_withdraw_limit: Decimal
    account_type: AccountTypes


class NewAccount(Account):
    balance: Decimal
    is_active: Optional[bool]
    person_id: UUID


class AccountOut(Account):
    id: UUID
    person: PersonSchema
    balance: Decimal
    created_at: datetime


class AccountBalance(BaseModel):
    person: PersonSchema
    balance: Decimal
