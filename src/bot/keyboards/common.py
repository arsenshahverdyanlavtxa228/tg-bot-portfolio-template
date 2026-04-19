from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.services.i18n import Translator


def main_menu_kb(t: Translator, *, has_cv: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t("menu-about"), callback_data="v:about")
    builder.button(text=t("menu-projects"), callback_data="v:projects")
    builder.button(text=t("menu-experience"), callback_data="v:experience")
    builder.button(text=t("menu-skills"), callback_data="v:skills")
    builder.button(text=t("menu-contacts"), callback_data="v:contacts")
    if has_cv:
        builder.button(text=t("menu-cv"), callback_data="v:cv")
    builder.button(text=t("menu-language"), callback_data="v:lang")
    builder.adjust(2, 2, 2, 1)
    return builder.as_markup()


def language_kb(t: Translator, current: str, prefix: str = "lang") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=("• " if current == "ru" else "") + t("language-ru"),
        callback_data=f"{prefix}:ru",
    )
    builder.button(
        text=("• " if current == "en" else "") + t("language-en"),
        callback_data=f"{prefix}:en",
    )
    builder.button(text=t("back"), callback_data="v:menu")
    builder.adjust(2, 1)
    return builder.as_markup()


def back_to_menu_kb(t: Translator) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=t("back"), callback_data="v:menu")]]
    )
