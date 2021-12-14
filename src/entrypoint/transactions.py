from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session

from src.service.transaction import deposit as service_deposit
from src.service.transaction import withdraw as service_withdraw
from src.dto.transaction import TransactionIn
from src.repository.database import get_db


router = APIRouter()


@router.post("/deposit", status_code=status.HTTP_202_ACCEPTED)
def deposit(deposit: TransactionIn, db: Session = Depends(get_db)) -> None:
    service_deposit(db, deposit)


@router.post("/withdraw", status_code=status.HTTP_202_ACCEPTED)
def withdraw(withdraw: TransactionIn, db: Session = Depends(get_db)) -> None:
    service_withdraw(db, withdraw)
