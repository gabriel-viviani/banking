from fastapi import APIRouter

from src.entrypoint import account, person, transactions

api_router = APIRouter()
api_router.include_router(account.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(person.router, prefix="/people", tags=["people"])
api_router.include_router(
    transactions.router, prefix="/transactions", tags=["transactions"]
)
