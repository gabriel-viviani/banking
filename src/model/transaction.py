from sqlalchemy import DateTime, ForeignKey, Column
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import relationship
from uuid import uuid4
import UUID

from config import generate_now
from build_app import Base


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    value = Column(MONEY, nullable=False)
    transaction_time = Column(DateTime, default=generate_now())
    account_id = Column(UUID(as_uuid=True), ForeignKey("account.id"))

    account = relationship("Account", back_populates="transactions")

    def __init__(self, value: MONEY, account_id: UUID) -> None:
        self.value = value
        self.account_id = account_id
