from sqlalchemy.dialects.postgresql import MONEY
from pydantic import BaseModel
from datetime import datetime
import UUID


class TransactionIn(BaseModel):
    value: MONEY
    account_id: UUID


class TransactionOut(BaseModel):
    value: MONEY
    transaction_time: datetime
