import pytest
from uuid import uuid4
from decimal import Decimal

from tests.helpers import (
    rand_negative_decimal,
    rand_positive_decimal,
)
from src.model.account import Account


def test_deposit(client, db, db_acc):
    transaction = {
        "value": str(rand_positive_decimal()),
        "account_id": str(db_acc.id),
    }

    acc_balance = db_acc.balance
    res = client.post("/transactions/deposit", json=transaction)

    assert res.status_code == 202

    acc = db.query(Account).filter_by(id=db_acc.id).first()

    assert acc.balance == (acc_balance + Decimal(transaction["value"]))


def test_withdraw_zero(client, db_acc):
    transaction = {"value": 0, "account_id": str(db_acc.id)}

    res = client.post("/transactions/withdraw", json=transaction)
    assert res.status_code == 405


def test_deposit_zero(client, db_acc):
    transaction = {"value": 0, "account_id": str(db_acc.id)}

    res = client.post("/transactions/deposit", json=transaction)
    assert res.status_code == 405


def test_withdraw_wrong_value(client, db_acc):
    transaction = {
        "value": str(rand_positive_decimal()),
        "account_id": str(db_acc.id),
    }

    res = client.post("/transactions/withdraw", json=transaction)
    assert res.status_code == 409


def test_deposit_wrong_value(client, db_acc):
    transaction = {
        "value": str(rand_negative_decimal()),
        "account_id": str(db_acc.id),
    }

    res = client.post("/transactions/deposit", json=transaction)
    assert res.status_code == 409


def test_deposit_acc_not_found(client):
    transaction = {
        "value": str(rand_positive_decimal()),
        "account_id": str(uuid4()),
    }

    res = client.post("/transactions/deposit", json=transaction)
    assert res.status_code == 404


def test_withdraw_acc_not_found(client):
    transaction = {
        "value": str(rand_negative_decimal()),
        "account_id": str(uuid4()),
    }

    res = client.post("/transactions/withdraw", json=transaction)
    assert res.status_code == 404


def test_withdraw_acc_blocked(client, db_acc, db):
    db_acc.is_active = False
    db.flush()

    transaction = {
        "value": str(rand_negative_decimal()),
        "account_id": str(db_acc.id),
    }

    res = client.post("/transactions/withdraw", json=transaction)
    assert res.status_code == 405


def test_deposit_acc_blocked(client, db_acc, db):
    db_acc.is_active = False
    db.flush()

    transaction = {
        "value": str(rand_positive_decimal()),
        "account_id": str(db_acc.id),
    }

    res = client.post("/transactions/deposit", json=transaction)
    assert res.status_code == 405


def test_withdraw(client, db, db_acc):
    transaction = {
        "value": str(rand_negative_decimal()),
        "account_id": str(db_acc.id),
    }

    acc_balance = db_acc.balance
    res = client.post("/transactions/withdraw", json=transaction)

    assert res.status_code == 202

    acc = db.query(Account).filter_by(id=db_acc.id).first()

    assert acc.balance == (acc_balance + Decimal(transaction["value"]))
