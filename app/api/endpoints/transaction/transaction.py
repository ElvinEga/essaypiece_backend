from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.api.endpoints.transaction.functions import (
    create_transaction,
    get_user_transactions,
    update_transaction_status, get_all_transactions
)
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionStatus
from typing import List

transaction_module = APIRouter()


# Create a transaction (deposit or withdrawal)
@transaction_module.post("/transactions/", response_model=TransactionRead)
def create_transaction_endpoint(user_id: int, transaction: TransactionCreate, db: Session = Depends(get_db)):
    return create_transaction(user_id, transaction, db)


# Get all transactions for a user
@transaction_module.get("/transactions/{user_id}", response_model=List[TransactionRead])
def get_transactions(user_id: int, db: Session = Depends(get_db)):
    return get_user_transactions(user_id, db)


# Update transaction status
@transaction_module.put("/transactions/{transaction_id}/status")
def update_transaction_status_endpoint(transaction_id: int, status: TransactionStatus,
                                       db: Session = Depends(get_db)):
    return update_transaction_status(transaction_id, status, db)


@transaction_module.get("/transactions/", response_model=List[TransactionRead])
def list_all_transactions(db: Session = Depends(get_db)):
    return get_all_transactions(db)


# Get transactions for a specific user
@transaction_module.get("/transactions/user/{user_id}", response_model=List[TransactionRead])
def list_user_transactions(user_id: int, db: Session = Depends(get_db)):
    return get_user_transactions(user_id, db)
