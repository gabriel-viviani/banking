from sqlalchemy.dialects.postgresql import MONEY
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
import UUID

from .person import PersonSchema


class AccountTypes(str, Enum):
    salary = "salary"
    savings = "savings"
    checking = "checking"


class Account(BaseModel):
    daily_withdraw_limit: MONEY
    account_type: AccountTypes


class NewAccount(Account):
    balance: Optional[MONEY]
    is_active: Optional[bool]
    person_id: UUID


class AccountOut(Account):
    id: UUID
    person: PersonSchema
    balance: MONEY
    created_at: datetime


class AccountBalance(BaseModel):
    person: PersonSchema
    balance: MONEY
