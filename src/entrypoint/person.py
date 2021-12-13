from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from typing import Any

from src.repository.database import get_db
from src.model.person import Person

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_people(db: Session = Depends(get_db)) -> Any:
    return db.query(Person).all()
