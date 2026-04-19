from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from bot.database import Repository
from bot.services.i18n import I18n


class I18nMiddleware(BaseMiddleware):
    """Resolves the translator for each update.

    Priority: profile.locale (admin setting) → user.language_code → default.
    """

    def __init__(self, i18n: I18n) -> None:
        self._i18n = i18n

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        repo: Repository | None = data.get("repo")
        locale = self._i18n.default_locale
        if repo is not None:
            profile = await repo.get_profile()
            if profile.locale in self._i18n.available:
                locale = profile.locale
            else:
                user: User | None = data.get("event_from_user")
                if user and user.language_code:
                    lc = user.language_code.split("-")[0]
                    if lc in self._i18n.available:
                        locale = lc
        data["t"] = self._i18n.get(locale)
        return await handler(event, data)
