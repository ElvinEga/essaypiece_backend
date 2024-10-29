import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.api.endpoints.transaction.functions import (
    create_transaction,
    get_user_transactions,
    update_transaction_status, get_all_transactions
)
from app.models.transaction import Transaction, Sign, TransactionType
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionStatus, TransactionOut
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


@transaction_module.post("/add_funds/paystack", response_model=TransactionOut)
def add_funds_paystack(client_id: int, amount: float, db: Session = Depends(get_db)):
    # Create a pending transaction for the Paystack deposit
    new_transaction = Transaction(
        transaction_number=str(uuid.uuid4()),  # temporary transaction number
        user_id=client_id,
        amount=amount,
        type="deposit",
        sign=Sign.positive,
        payment_method="paystack",
        status=TransactionStatus.pending,  # pending
        description="Paystack deposit"
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    # Initiate the Paystack payment (simplified, assuming Paystack client is already configured)
    # paystack_response = paystack_client.initiate_payment(amount, client_id)

    # Return transaction details
    return new_transaction


@transaction_module.post("/paystack/callback")
def paystack_callback(transaction_id: str, paystack_transaction_id: str, db: Session = Depends(get_db)):
    # Fetch the transaction by temporary transaction_id
    transaction = db.query(Transaction).filter(Transaction.transaction_number == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Confirm transaction is a Paystack payment
    if transaction.type != TransactionType.deposit:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    # Update transaction status and transaction number with Paystack ID
    transaction.status = TransactionStatus.completed
    transaction.transaction_number = paystack_transaction_id  # Update with Paystack's transaction ID
    db.commit()

    # Update user balance
    user = db.query(User).filter(User.id == transaction.user_id).first()
    if user:
        user.balance += transaction.amount
        db.commit()

    return {"status": "success", "message": "Transaction confirmed and balance updated."}
