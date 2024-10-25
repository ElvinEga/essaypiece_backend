import uuid

from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.transaction import Transaction, TransactionStatus
from app.schemas.transaction import TransactionCreate
from fastapi import HTTPException, status


# Create a new transaction
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    new_transaction = Transaction(
        transaction_number=str(uuid.uuid4()),  # Generate a unique transaction number
        user_id=transaction.user_id,
        amount=transaction.amount,
        type=transaction.type,
        sign=transaction.sign,
        payment_method=transaction.payment_method,
        status=transaction.status,
        description=transaction.description
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


# Get transactions for a specific user
def get_user_transactions(user_id: int, db: Session):
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()


# Update transaction status
def update_transaction_status(transaction_id: int, status: TransactionStatus, db: Session):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    db_transaction.status = status
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


# Get all transactions
def get_all_transactions(db: Session):
    return db.query(Transaction).all()


# Get transactions for a specific user
def get_user_transactions(user_id: int, db: Session):
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for the specified user")
    return transactions
