from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.database import Repository, SessionFactory


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, factory: SessionFactory) -> None:
        self._factory = factory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self._factory.session() as session:
            data["repo"] = Repository(session)
            data["session"] = session
            return await handler(event, data)
