from sqlalchemy import ForeignKey, String, Date, Column
from sqlalchemy.orm import relationship
from uuid import uuid4
import UUID

from build_app import Base


class Person(Base):
    __tablename__ = "person"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)

    account = relationship("Account", back_populates="person", uselist=False)