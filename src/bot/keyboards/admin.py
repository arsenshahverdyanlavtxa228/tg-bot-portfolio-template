from collections.abc import Sequence

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.database.models import Contact, Experience, Project, Skill
from bot.services.i18n import Translator

CONTACT_KINDS: tuple[tuple[str, str], ...] = (
    ("email", "📧 Email"),
    ("telegram", "✈️ Telegram"),
    ("github", "🐙 GitHub"),
    ("linkedin", "💼 LinkedIn"),
    ("website", "🌐 Website"),
    ("phone", "📞 Phone"),
)


def admin_menu_kb(t: Translator) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t("admin-set-name"), callback_data="a:set:name")
    builder.button(text=t("admin-set-headline"), callback_data="a:set:headline")
    builder.button(text=t("admin-set-bio"), callback_data="a:set:bio")
    builder.button(text=t("admin-set-photo"), callback_data="a:set:photo")
    builder.button(text=t("admin-set-cv"), callback_data="a:set:cv")
    builder.button(text=t("admin-projects"), callback_data="a:projects")
    builder.button(text=t("admin-experience"), callback_data="a:experience")
    builder.button(text=t("admin-skills"), callback_data="a:skills")
    builder.button(text=t("admin-contacts"), callback_data="a:contacts")
    builder.button(text=t("admin-language"), callback_data="a:language")
    builder.adjust(2, 2, 1, 2, 2, 1)
    return builder.as_markup()


def admin_projects_kb(t: Translator, projects: Sequence[Project]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for p in projects:
        builder.button(text=f"🗑 {p.title}", callback_data=f"a:project:del:{p.id}")
    builder.button(text=t("add"), callback_data="a:project:add")
    builder.button(text=t("back"), callback_data="a:menu")
    builder.adjust(1)
    return builder.as_markup()


def admin_experience_kb(t: Translator, items: Sequence[Experience]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for x in items:
        builder.button(text=f"🗑 {x.role} @ {x.company}", callback_data=f"a:exp:del:{x.id}")
    builder.button(text=t("add"), callback_data="a:exp:add")
    builder.button(text=t("back"), callback_data="a:menu")
    builder.adjust(1)
    return builder.as_markup()


def admin_skills_kb(t: Translator, items: Sequence[Skill]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for x in items:
        builder.button(text=f"🗑 {x.name}", callback_data=f"a:skill:del:{x.id}")
    builder.button(text=t("add"), callback_data="a:skill:add")
    builder.button(text=t("back"), callback_data="a:menu")
    builder.adjust(2)
    return builder.as_markup()


def admin_contacts_kb(t: Translator, current: Sequence[Contact]) -> InlineKeyboardMarkup:
    filled = {c.kind: c.value for c in current}
    builder = InlineKeyboardBuilder()
    for kind, label in CONTACT_KINDS:
        mark = "✅ " if kind in filled else ""
        builder.button(text=f"{mark}{label}", callback_data=f"a:contact:set:{kind}")
    for kind in filled:
        builder.button(text=f"🗑 {kind}", callback_data=f"a:contact:del:{kind}")
    builder.button(text=t("back"), callback_data="a:menu")
    builder.adjust(2)
    return builder.as_markup()


def admin_languages_kb(t: Translator, current: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=("• " if current == "ru" else "") + t("language-ru"),
        callback_data="a:lang:ru",
    )
    builder.button(
        text=("• " if current == "en" else "") + t("language-en"),
        callback_data="a:lang:en",
    )
    builder.button(text=t("back"), callback_data="a:menu")
    builder.adjust(2, 1)
    return builder.as_markup()


def cancel_kb(t: Translator) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=t("cancel"))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def skip_cancel_kb(t: Translator) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=t("skip"))
    builder.button(text=t("cancel"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
