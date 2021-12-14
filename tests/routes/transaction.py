import pytest

from tests.helpers import random_decimal, random_name
from src.dto.transaction import TransactionIn
from src.model.account import Account


def test_withdraw(client, db, db_acc):
    transaction = TransactionIn(
        value=-abs(random_decimal()), account_id=db_acc.id
    )

    acc_balance = db_acc.balance
    res = client.post("/transactions/withdraw", json=transaction)

    assert res.status_code == 202

    acc = db.query(Account).filter_by(id=db_acc.id).first()

    assert acc.balance is (acc_balance + transaction.value)


def test_deposit(client, db, db_acc):
    transaction = TransactionIn(value=random_decimal(), account_id=db_acc.id)

    acc_balance = db_acc.balance
    res = client.post("/transactions/deposit", json=transaction)

    assert res.status_code == 202

    acc = db.query(Account).filter_by(id=db_acc.id).first()

    assert acc.balance is (acc_balance + transaction.value)


def test_withdraw_zero(client, db_acc):
    transaction = TransactionIn(value=0, account_id=db_acc.id)

    res = client.post("/transactions/withdraw", json=transaction)
    assert res.status_code == 405


def test_deposit_zero(client, db_acc):
    transaction = TransactionIn(value=0, account_id=db_acc.id)

    res = client.post("/transactions/deposit", json=transaction)
    assert res.status_code == 405


def test_withdraw_wrong_value(client, db_acc):
    transaction = TransactionIn(value=random_decimal(), account_id=db_acc.id)

    res = client.post("/transactions/withdraw", json=transaction)
    assert res.status_code == 409


def test_deposit_wrong_value(client, db_acc):
    transaction = TransactionIn(
        value=-abs(random_decimal()), account_id=db_acc.id
    )

    res = client.post("/transactions/deposit", json=transaction)
    assert res.status_code == 409


def test_deposit_acc_not_found(client):
    transaction = TransactionIn(
        value=random_decimal(), account_id=random_name()
    )

    res = client.post("/transactions/deposit", json=transaction)
    assert res.status_code == 404


def test_withdraw_acc_not_found(client):
    transaction = TransactionIn(
        value=-abs(random_decimal()), account_id=random_name()
    )

    res = client.post("/transactions/withdraw", json=transaction)
    assert res.status_code == 404


def test_withdraw_acc_blocked(client, db_acc, db):
    db_acc.is_active = False
    db.flush()
    db.refresh(db_acc)

    transaction = TransactionIn(
        value=-abs(random_decimal()), account_id=db_acc.id
    )

    res = client.post("/transactions/withdraw", json=transaction)
    assert res.status_code == 405


def test_deposit_acc_blocked(client, db_acc, db):
    db_acc.is_active = False
    db.flush()
    db.refresh(db_acc)

    transaction = TransactionIn(value=random_decimal(), account_id=db_acc.id)

    res = client.post("/transactions/deposit", json=transaction)
    assert res.status_code == 405
