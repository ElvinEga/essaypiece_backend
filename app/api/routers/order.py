from fastapi import APIRouter
from app.api.endpoints.order import order

order_router = APIRouter()

order_router.include_router(order.order_module, prefix="/orders", tags=["orders"])
