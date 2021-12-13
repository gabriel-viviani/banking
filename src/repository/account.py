from sqlalchemy.orm import Session
from typing import Any

from src.dto.account import AccountTypes, NewAccount
from src.model.account import Account


def get_account_by_person_id(
    db: Session, person_id: str, acc_type: AccountTypes
) -> Any:
    account = (
        db.query(Account)
        .filter_by(person_id=person_id, account_type=acc_type)
        .all()
    )

    return account


def save_account(db: Session, acc: NewAccount) -> None:
    account = Account(
        balance=acc.balance,
        daily_withdraw_limit=acc.daily_withdraw_limit,
        account_type=acc.account_type,
        person_id=str(acc.person_id),
    )

    db.add(account)
    db.commit()


def get_account_by_id(db: Session, id: str) -> Any:
    return db.query(Account).filter_by(id=id).first()


def block_account(db: Session, account: Account) -> None:
    account.is_active = False
    db.add(account)
    db.commit()
