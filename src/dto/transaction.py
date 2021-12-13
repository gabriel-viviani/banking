from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from uuid import UUID


class TransactionIn(BaseModel):
    value: Decimal
    account_id: UUID


class TransactionOut(BaseModel):
    value: Decimal
    transaction_time: datetime
