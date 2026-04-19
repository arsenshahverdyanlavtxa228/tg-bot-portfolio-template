from aiogram import Dispatcher

from bot.handlers import admin, visitor


def register_all(dp: Dispatcher) -> None:
    dp.include_router(admin.router)
    dp.include_router(visitor.router)


__all__ = ["register_all"]
