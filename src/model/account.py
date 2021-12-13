from sqlalchemy import (
    Boolean,
    DateTime,
    Column,
    Enum,
    ForeignKey,
    DECIMAL,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from decimal import Decimal
from uuid import uuid4

from src.dto.account import AccountTypes
from src.repository.database import Base
from src.config import generate_now


class Account(Base):
    __tablename__ = "account"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    balance = Column(DECIMAL(30, 10), default="0")
    daily_withdraw_limit = Column(DECIMAL(30, 10))
    is_active = Column(Boolean, default=True)
    account_type = Column(Enum(AccountTypes), nullable=False)
    created_at = Column(DateTime, default=generate_now())
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id"))

    person = relationship("Person", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

    def __init__(
        self,
        balance: Decimal,
        daily_withdraw_limit: Decimal,
        account_type: AccountTypes,
        person_id: str,
    ) -> None:
        self.balance = balance
        self.daily_withdraw_limit = daily_withdraw_limit
        self.account_type = account_type
        self.person_id = person_id
