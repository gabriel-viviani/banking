from sqlalchemy import (
    Column,
    String,
    Date,
)
from src.repository.database import Base, SessionLocal
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import date
from uuid import uuid4


class Person(Base):
    __tablename__ = "person"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)

    accounts = relationship("Account", back_populates="person")

    def __init__(self, name: str, cpf: str, birth_date: date) -> None:
        self.name = name
        self.cpf = cpf
        self.birth_date = birth_date


def create_mock_data() -> None:
    db = SessionLocal()

    people = db.query(Person).all()
    if len(people) > 0:
        return

    person_1 = Person(
        name="Gabriel Viviani", cpf="12081985450", birth_date=date(1998, 2, 20)
    )

    person_2 = Person(
        name="Adriana Raquel", cpf="345187287391", birth_date=date(1958, 8, 20)
    )

    db.add(person_1)
    db.add(person_2)

    db.commit()
    db.close()


create_mock_data()
