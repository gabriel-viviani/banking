from build_app import application as app
from fastapi import Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from build_app import get_db
from datetime import date

from dto.account import NewAccount, AccountBalance, AccountOut
from dto.transaction import TransactionOut
from service import create_account as create
from service import get_balance as balance
from service import block, bank_statement


@app.post("/account/", status_code=status.HTTP_201_CREATED)
async def create_account(
    new_acc: NewAccount, db: Session = Depends(get_db)
) -> None:
    await create(db, new_acc)


@app.get("/account/{account_id}/balance", status_code=status.HTTP_200_OK)
async def get_balance(
    account_id: str, db: Session = Depends(get_db)
) -> AccountBalance:
    return await balance(db, account_id)


@app.put("/account/{account_id}/block", status_code=status.HTTP_200_OK)
async def block_account(account_id: str, db: Session = Depends(get_db)) -> None:
    await block(db, account_id)


@app.get("/account/{account_id}/transactions", status_code=status.HTTP_200_OK)
async def get_bank_statement(
    account_id: str,
    start_date: Optional[date],
    end_date: Optional[date],
    db: Session = Depends(get_db),
) -> List[TransactionOut]:
    return await bank_statement(account_id, db, start_date, end_date)
