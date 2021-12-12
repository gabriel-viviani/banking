from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal

from repository.account import get_account_by_id
from repository.transaction import deposit as repository_deposit
from repository.transaction import withdraw as repository_withdraw
from dto.transaction import TransactionIn


async def deposit(db: Session, deposit: TransactionIn) -> None:
    if Decimal(deposit.value) < 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are trying to withdraw, use another resource.",
        )

    acc = await get_account_by_id(deposit.account_id)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account {deposit.account_id} doesn't exists.",
        )

    if not acc.is_active:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Account is blocked, please contact carrier.",
        )

    repository_deposit(db, deposit)


async def withdraw(db: Session, withdraw: TransactionIn) -> None:
    if Decimal(withdraw.value) > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are trying to deposit, use another resource.",
        )

    acc = await get_account_by_id(withdraw.account_id)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account {withdraw.account_id} doesn't exists.",
        )

    if not acc.is_active:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Account is blocked, please contact carrier.",
        )

    repository_withdraw(db, withdraw)
