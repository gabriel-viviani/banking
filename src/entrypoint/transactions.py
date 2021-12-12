from build_app import application as app
from fastapi import Depends, status
from sqlalchemy.orm import Session
from build_app import get_db

from service.transaction import deposit as service_deposit
from service.transaction import withdraw as service_withdraw
from dto.account import TransactionIn


@app.post("/transaction/deposit/", status_code=status.HTTP_202_ACCEPTED)
async def deposit(
    deposit: TransactionIn, db: Session = Depends(get_db)
) -> None:
    await service_deposit(db, deposit)


@app.post("transaction/withdraw/", status_code=status.HTTP_202_ACCEPTED)
async def withdraw(
    withdraw: TransactionIn, db: Session = Depends(get_db)
) -> None:
    await service_withdraw(db, withdraw)
