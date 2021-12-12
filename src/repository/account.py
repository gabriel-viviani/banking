from sqlalchemy.orm import Session
from typing import Any
import UUID

from dto.account import AccountOut, AccountTypes, NewAccount
from dto.person import PersonSchema
from model.account import Account


async def get_account_by_person_id(
    db: Session, person_id: UUID, acc_type: AccountTypes
) -> Any:
    account = await db.query(Account).filter_by(
        person_id=person_id, account_type=acc_type
    )

    return account


def save_account(db: Session, acc: NewAccount) -> None:
    account = Account(
        balance=acc.balance,
        daily_withdraw_limit=acc.daily_withdraw_limit,
        account_type=acc.account_type,
        person_id=acc.person_id,
    )

    db.add(account)
    db.commit()


async def get_account_by_id(db: Session, id: UUID) -> Any:
    return await db.query(Account).filter_by(id=id)


def block_account(db: Session, account: Account) -> None:
    account.is_active = False
    db.add(account)
    db.commit()
