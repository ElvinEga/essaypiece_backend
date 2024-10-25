from sqlalchemy.orm import Session
from app.models.transaction import Transaction, TransactionStatus
from app.schemas.transaction import TransactionCreate
from fastapi import HTTPException, status


# Create a new transaction
def create_transaction(user_id: int, transaction: TransactionCreate, db: Session):
    db_transaction = Transaction(
        user_id=user_id,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        description=transaction.description,
        status=TransactionStatus.pending,  # Default to pending on creation
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


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
