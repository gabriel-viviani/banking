from sqlalchemy import DateTime, ForeignKey, Column, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from decimal import Decimal
from uuid import uuid4

from src.repository.database import Base
from src.config import generate_now


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    value = Column(DECIMAL(30, 10), nullable=False)
    transaction_time = Column(DateTime, default=generate_now())
    account_id = Column(UUID(as_uuid=True), ForeignKey("account.id"))

    account = relationship("Account", back_populates="transactions")

    def __init__(self, value: Decimal, account_id: str) -> None:
        self.value = value
        self.account_id = account_id
