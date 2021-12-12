from sqlalchemy.orm import Session
from typing import Any
from datetime import date
import UUID

from dto.transaction import TransactionIn
from model.transaction import Transaction


def deposit(db: Session, deposit: TransactionIn) -> None:
    transaction = Transaction(
        value=deposit.value, account_id=deposit.account_id
    )

    db.add(transaction)
    db.commit()


def withdraw(db: Session, deposit: TransactionIn) -> None:
    transaction = Transaction(
        value=deposit.value, account_id=deposit.account_id
    )

    db.add(transaction)
    db.commit()


async def get_bank_statement_date_filtered(
    account_id: UUID,
    db: Session,
    start_date: date,
    end_date: date,
) -> Any:
    return await db.query(Transaction).filter(
        and_(
            Transaction.account_id=account_id,
            Transaction.transaction_time.between(start_date, end_date)
        )
    )

async def get_bank_statement(account_id: UUID, db: Session) -> Any:
    return await db.query(Transaction).filter_by(account_id=account_id)
