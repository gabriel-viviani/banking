from sqlalchemy import Boolean, DateTime, Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import relationship
from uuid import uuid4
import UUID

from dto.account import AccountTypes
from config import generate_now
from build_app import Base


class Account(Base):
    __tablename__ = "account"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    balance = Column(MONEY, default="0")
    daily_withdraw_limit = Column(MONEY)
    is_active = Column(Boolean, default=True)
    account_type = Column(Enum(AccountTypes), nullable=False)
    created_at = Column(DateTime, default=generate_now())
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id"), unique=True)

    person = relationship("Person", back_populates="account")
    transactions = relationship("Account", back_populates="account")

    def __init__(
        self,
        balance: MONEY,
        daily_withdraw_limit: MONEY,
        account_type: AccountTypes,
        person_id: UUID,
    ) -> None:
        self.balance = balance
        self.daily_withdraw_limit = (daily_withdraw_limit,)
        self.account_type = account_type
        self.person_id = person_id
