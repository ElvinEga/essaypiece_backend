from fastapi import APIRouter
from app.api.endpoints.transaction import transaction as transaction_router

transactionRouter = APIRouter()

transactionRouter.include_router(transaction_router.transaction_module, prefix="/transactions", tags=["transactions"])
