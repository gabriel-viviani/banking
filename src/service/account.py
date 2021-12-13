from sqlalchemy.dialects.postgresql import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from src.repository.account import (
    get_account_by_person_id,
    save_account,
    get_account_by_id,
    block_account,
)
from src.repository.transaction import (
    get_bank_statement,
    get_bank_statement_date_filtered,
)

from src.dto.account import NewAccount, AccountBalance
from src.dto.transaction import TransactionOut
from src.dto.account import PersonSchema


async def create_account(db: Session, new_acc: NewAccount) -> None:
    account = get_account_by_person_id(
        db, str(new_acc.person_id), new_acc.account_type
    )
    if account:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Account of person {new_acc.person_id} of type {new_acc.account_type}, already exists.",
        )

    save_account(db, new_acc)


async def get_balance(db: Session, account_id: str) -> AccountBalance:
    account = get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with {account_id} as id, not found.",
        )

    if not account.is_active:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Account is blocked, please contact carrier.",
        )

    return AccountBalance(
        balance=account.balance,
        person=PersonSchema(
            cpf=account.person.cpf,
            name=account.person.name,
            birth_date=account.person.birth_date,
        ),
    )


async def block(db: Session, account_id: str) -> None:
    account = get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with {account_id} as id, not found.",
        )

    if not account.is_active:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Account is already blocked, please contact carrier.",
        )

    block_account(db, account)


async def bank_statement(
    account_id: str,
    db: Session,
    start_date: Optional[date],
    end_date: Optional[date],
) -> List[TransactionOut]:
    account = get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with {account_id} as id, not found.",
        )

    if not account.is_active:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Account is blocked, please contact carrier.",
        )

    if start_date and end_date:
        bank_statement = get_bank_statement_date_filtered(
            account_id, db, start_date, end_date
        )
    else:
        bank_statement = get_bank_statement(account_id, db)

    return [
        TransactionOut(
            value=transaction.value,
            transaction_time=transaction.transaction_time,
        )
        for transaction in bank_statement
    ]
