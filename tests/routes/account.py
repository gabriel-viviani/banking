import pytest
from uuid import uuid4
from decimal import Decimal

from tests.helpers import (
    rand_positive_decimal,
    rand_negative_decimal,
    random_name,
    random_valid_cpf,
    rand_date,
)
from src.model.account import Account, AccountTypes
from src.model.transaction import Transaction
from src.model.person import Person


def test_account_balance(db_acc, client):
    res = client.get(f"/accounts/{db_acc.id}/balance")
    assert res.status_code == 200

    account = res.json()
    assert account["balance"] is not None


def test_account_transactions(db_acc, client, db):
    _first_transaction = Transaction(
        value=rand_negative_decimal(), account_id=db_acc.id
    )
    _second_transaction = Transaction(
        value=rand_positive_decimal(), account_id=db_acc.id
    )

    db.add(_first_transaction)
    db.add(_second_transaction)
    db.flush()

    res = client.get(f"/accounts/{db_acc.id}/transactions")
    assert res.status_code == 200

    transactions = res.json()
    assert len(transactions) > 0


def test_get_acc_balance_blocked_acc(db_acc, db, client):
    db_acc.is_active = False
    db.flush()
    db.refresh(db_acc)

    res = client.get(f"/accounts/{db_acc.id}/balance")
    assert res.status_code == 405

    db_acc.is_active = True
    db.flush()
    db.refresh(db_acc)


def test_get_acc_balance_account_not_found(client):
    res = client.get(f"/accounts/{uuid4()}/balance")
    assert res.status_code == 404


def test_get_acc_transactions_blocked_acc(db_acc, db, client):
    db_acc.is_active = False
    db.add(db_acc)
    db.flush()
    db.refresh(db_acc)

    res = client.get(f"/accounts/{db_acc.id}/transactions")
    assert res.status_code == 405

    db_acc.is_active = True
    db.flush()
    db.refresh(db_acc)


def test_get_acc_transactions_account_not_found(client):
    res = client.get(f"/accounts/{uuid4()}/transactions")
    assert res.status_code == 404


def test_create_acc(client, db):
    _person = Person(random_name(), random_valid_cpf(), rand_date())
    db.add(_person)
    db.flush()
    db.refresh(_person)

    _new_acc = {
        "balance": str(rand_positive_decimal()),
        "person_id": str(_person.id),
        "daily_withdraw_limit": str(rand_positive_decimal()),
        "account_type": AccountTypes.checking,
    }

    acc_number = len(db.query(Account).all())

    res = client.post("/accounts/", json=_new_acc)
    assert res.status_code == 201

    acc_number_after_insert = len(db.query(Account).all())
    assert acc_number_after_insert is (acc_number + 1)


def test_create_acc_conflict(client, db):
    _person = Person(random_name(), random_valid_cpf(), rand_date())
    db.add(_person)
    db.flush()
    db.refresh(_person)

    _new_acc = Account(
        balance=rand_positive_decimal(),
        person_id=_person.id,
        daily_withdraw_limit=rand_positive_decimal(),
        account_type=AccountTypes.checking,
    )

    db.add(_new_acc)
    db.flush()

    new_acc = {
        "balance": str(rand_positive_decimal()),
        "person_id": str(_person.id),
        "daily_withdraw_limit": str(rand_positive_decimal()),
        "account_type": AccountTypes.checking,
    }

    res = client.post("/accounts/", json=new_acc)
    assert res.status_code == 409


def test_block_acc(client, db_acc, db):
    res = client.put(f"/accounts/{db_acc.id}/block")
    assert res.status_code == 200

    _acc = db.query(Account).filter_by(id=db_acc.id).first()
    assert _acc.is_active is False


def test_block_acc_not_found(client):
    res = client.put(f"/accounts/{uuid4()}/block")
    assert res.status_code == 404


def test_block_acc_already_blocked(client, db, db_acc):
    db_acc.is_active = False
    db.flush()
    db.refresh(db_acc)

    res = client.put(f"/accounts/{db_acc.id}/block")
    assert res.status_code == 405
