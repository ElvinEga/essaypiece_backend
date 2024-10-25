from fastapi import APIRouter

from app.api.routers.order import order_router
from app.api.routers.transaction import transactionRouter
from app.api.routers.user import user_router

router = APIRouter()

router.include_router(user_router)
router.include_router(transactionRouter)
router.include_router(order_router)


