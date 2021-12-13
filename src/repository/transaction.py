from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date
from typing import Any

from src.dto.transaction import TransactionIn
from src.model.transaction import Transaction


def deposit(db: Session, deposit: TransactionIn) -> None:
    transaction = Transaction(
        value=deposit.value, account_id=str(deposit.account_id)
    )

    db.add(transaction)
    db.commit()


def withdraw(db: Session, deposit: TransactionIn) -> None:
    transaction = Transaction(
        value=deposit.value, account_id=str(deposit.account_id)
    )

    db.add(transaction)
    db.commit()


def get_bank_statement_date_filtered(
    account_id: str,
    db: Session,
    start_date: date,
    end_date: date,
) -> Any:
    return (
        db.query(Transaction)
        .filter(
            and_(
                Transaction.account_id == account_id,
                Transaction.transaction_time.between(start_date, end_date),
            )
        )
        .all()
    )


def get_bank_statement(account_id: str, db: Session) -> Any:
    return db.query(Transaction).filter_by(account_id=account_id).all()
