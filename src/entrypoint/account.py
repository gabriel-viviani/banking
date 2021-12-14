from fastapi import Depends, status, APIRouter, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from src.service.account import create_account as create
from src.dto.account import NewAccount, AccountBalance
from src.service.account import get_balance as balance
from src.service.account import block, bank_statement
from src.dto.transaction import TransactionOut
from src.repository.database import get_db

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_account(
    new_acc: NewAccount, db: Session = Depends(get_db)
) -> None:
    await create(db, new_acc)


@router.get(
    "/{account_id}/balance",
    status_code=status.HTTP_200_OK,
    response_model=AccountBalance,
)
async def get_balance(
    account_id: str, db: Session = Depends(get_db)
) -> AccountBalance:
    return await balance(db, account_id)


@router.put("/{account_id}/block", status_code=status.HTTP_200_OK)
async def block_account(account_id: str, db: Session = Depends(get_db)) -> None:
    await block(db, account_id)


@router.get(
    "/{account_id}/transactions",
    status_code=status.HTTP_200_OK,
    response_model=List[TransactionOut],
)
async def get_bank_statement(
    account_id: str,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
) -> List[TransactionOut]:
    return await bank_statement(account_id, db, start_date, end_date)
