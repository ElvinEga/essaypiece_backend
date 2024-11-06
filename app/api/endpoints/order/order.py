import json
import os
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import Client
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, OrderStatus
from app.models.order import Order
from app.core.dependencies import get_db

order_module = APIRouter()

ORDER_OPTIONS_FILE = os.path.join(os.path.dirname(__file__), "../../../data/order_options.json")


@order_module.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = Order(
        product=order.product,
        deadline=order.deadline,
        language=order.language,
        level=order.level,
        service=order.service,
        quantity=order.quantity,
        space=order.space,
        words_count=order.words_count,
        size_type=order.size_type,
        topic=order.topic,
        description=order.description,
        subject=order.subject,
        number_of_sources=order.number_of_sources,
        style=order.style,
        is_private=order.is_private,
        client_id=order.client_id,
        status=order.status  # Can be draft, open, or closed
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@order_module.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in order_update.dict(exclude_unset=True).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)

    return order


@order_module.patch("/{order_id}", response_model=OrderResponse)
def patch_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in order_update.dict(exclude_unset=True).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)

    return order


@order_module.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()

    return {"message": "Order deleted successfully"}


@order_module.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@order_module.get("/", response_model=List[OrderResponse])
def list_all_orders(db: Session = Depends(get_db), status: Optional[OrderStatus] = None):
    query = db.query(Order)

    if status:
        query = query.filter(Order.status == status)

    return query.all()


@order_module.get("/users/{user_id}/orders", response_model=List[OrderResponse])
def list_orders_by_user(user_id: str, db: Session = Depends(get_db), status: Optional[OrderStatus] = None):
    query = db.query(Order).filter(Order.client_id == user_id)

    if status:
        query = query.filter(Order.status == status)

    return query.all()


@order_module.get("/order_options/")
async def get_order_options():
    try:
        with open(ORDER_OPTIONS_FILE, "r") as file:
            order_options = json.load(file)
        return order_options
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Order options file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON file")
