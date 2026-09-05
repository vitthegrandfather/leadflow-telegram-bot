from aiogram import Dispatcher

from app.handlers.admin import router as admin_router
from app.handlers.customer import router as customer_router
from app.handlers.errors import register_error_handlers


def setup_routers(dp: Dispatcher) -> None:
    dp.include_router(admin_router)
    dp.include_router(customer_router)
    register_error_handlers(dp)
