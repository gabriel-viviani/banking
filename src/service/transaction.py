from sqlalchemy.dialects.postgresql import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.repository.transaction import withdraw as repository_withdraw
from src.repository.transaction import deposit as repository_deposit
from src.repository.account import get_account_by_id
from src.dto.transaction import TransactionIn
from src.model.account import Account


async def deposit(db: Session, deposit: TransactionIn) -> None:
    if deposit.value == 0:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="You cannot deposit 0.",
        )

    if deposit.value < 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are trying to withdraw, use another resource.",
        )

    acc = transaction_in_check_business_rules(db, deposit)

    repository_deposit(db, deposit)
    acc.balance = acc.balance + deposit.value
    db.commit()


async def withdraw(db: Session, withdraw: TransactionIn) -> None:
    if withdraw.value == 0:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="You cannot withdraw 0.",
        )

    if withdraw.value > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are trying to deposit, use another resource.",
        )

    acc = transaction_in_check_business_rules(db, withdraw)

    repository_withdraw(db, withdraw)
    acc.balance = acc.balance + withdraw.value
    db.commit()


def transaction_in_check_business_rules(
    db: Session, transaction: TransactionIn
) -> Account:
    acc: Account = get_account_by_id(db, str(transaction.account_id))
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account {transaction.account_id} doesn't exists.",
        )

    if not acc.is_active:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Account is blocked, please contact carrier.",
        )

    return acc
