from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from bot.database import Repository
from bot.keyboards.common import back_to_menu_kb, language_kb, main_menu_kb
from bot.services.i18n import Translator

router = Router(name="visitor")


def _owner_label(repo_name: str | None) -> str:
    return repo_name if repo_name else "—"


async def _render_menu(message: Message, repo: Repository, t: Translator) -> None:
    profile = await repo.get_profile()
    name = profile.full_name or ""
    viewer = message.from_user.full_name if message.from_user else ""
    if profile.full_name:
        text = t("start-welcome", name=viewer or "friend", owner=name)
    else:
        text = t("start-welcome-empty")
    await message.answer(
        text,
        reply_markup=main_menu_kb(t, has_cv=bool(profile.cv_file_id)),
        parse_mode=ParseMode.HTML,
    )


@router.message(CommandStart())
async def on_start(message: Message, repo: Repository, t: Translator) -> None:
    if message.from_user:
        await repo.log_visitor(message.from_user.id, message.from_user.username)
    await _render_menu(message, repo, t)


@router.callback_query(F.data == "v:menu")
async def back_to_menu(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    if isinstance(cq.message, Message):
        await cq.message.delete()
        await _render_menu(cq.message, repo, t)
    await cq.answer()


@router.callback_query(F.data == "v:about")
async def show_about(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    profile = await repo.get_profile()
    if not profile.full_name and not profile.bio:
        await cq.answer(t("about-empty"), show_alert=True)
        return

    parts: list[str] = []
    if profile.full_name:
        parts.append(t("about-header", name=profile.full_name))
    if profile.headline:
        parts.append(t("about-headline", headline=profile.headline))
    if profile.bio:
        parts.append("")
        parts.append(profile.bio)
    text = "\n".join(parts)

    if isinstance(cq.message, Message):
        await cq.message.delete()
        if profile.photo_file_id:
            await cq.message.answer_photo(
                photo=profile.photo_file_id,
                caption=text,
                reply_markup=back_to_menu_kb(t),
                parse_mode=ParseMode.HTML,
            )
        else:
            await cq.message.answer(
                text,
                reply_markup=back_to_menu_kb(t),
                parse_mode=ParseMode.HTML,
            )
    await cq.answer()


@router.callback_query(F.data == "v:projects")
async def show_projects(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    projects = await repo.list_projects()
    if not projects:
        await cq.answer(t("projects-empty"), show_alert=True)
        return

    if not isinstance(cq.message, Message):
        await cq.answer()
        return

    await cq.message.delete()
    for p in projects:
        parts = [t("project-title", title=p.title), "", p.description]
        if p.url:
            parts.append("")
            parts.append(t("project-link", url=p.url))
        caption = "\n".join(parts)
        if p.photo_file_id:
            await cq.message.answer_photo(
                photo=p.photo_file_id, caption=caption, parse_mode=ParseMode.HTML
            )
        else:
            await cq.message.answer(caption, parse_mode=ParseMode.HTML)
    await cq.message.answer("—", reply_markup=back_to_menu_kb(t))
    await cq.answer()


@router.callback_query(F.data == "v:experience")
async def show_experience(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    items = await repo.list_experiences()
    if not items:
        await cq.answer(t("experience-empty"), show_alert=True)
        return

    lines: list[str] = []
    for x in items:
        lines.append(t("experience-title", role=x.role, company=x.company))
        lines.append(t("experience-period", period=x.period))
        if x.description:
            lines.append(x.description)
        lines.append("")

    if isinstance(cq.message, Message):
        await cq.message.delete()
        await cq.message.answer(
            "\n".join(lines).strip(),
            reply_markup=back_to_menu_kb(t),
            parse_mode=ParseMode.HTML,
        )
    await cq.answer()


@router.callback_query(F.data == "v:skills")
async def show_skills(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    skills = await repo.list_skills()
    if not skills:
        await cq.answer(t("skills-empty"), show_alert=True)
        return
    text = t("skills-header") + "\n\n" + " • ".join(s.name for s in skills)
    if isinstance(cq.message, Message):
        await cq.message.delete()
        await cq.message.answer(text, reply_markup=back_to_menu_kb(t), parse_mode=ParseMode.HTML)
    await cq.answer()


@router.callback_query(F.data == "v:contacts")
async def show_contacts(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    contacts = await repo.list_contacts()
    if not contacts:
        await cq.answer(t("contacts-empty"), show_alert=True)
        return
    lines = [f"<b>{c.kind.capitalize()}:</b> {c.value}" for c in contacts]
    if isinstance(cq.message, Message):
        await cq.message.delete()
        await cq.message.answer(
            "\n".join(lines),
            reply_markup=back_to_menu_kb(t),
            parse_mode=ParseMode.HTML,
        )
    await cq.answer()


@router.callback_query(F.data == "v:cv")
async def show_cv(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    profile = await repo.get_profile()
    if not profile.cv_file_id:
        await cq.answer(t("cv-empty"), show_alert=True)
        return
    if isinstance(cq.message, Message):
        await cq.message.answer_document(document=profile.cv_file_id)
    await cq.answer()


@router.callback_query(F.data == "v:lang")
async def show_lang(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    profile = await repo.get_profile()
    if isinstance(cq.message, Message):
        await cq.message.edit_text(
            t("menu-language"),
            reply_markup=language_kb(t, current=profile.locale, prefix="v:lang:set"),
        )
    await cq.answer()


@router.callback_query(F.data.startswith("v:lang:set:"))
async def set_lang(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    locale = (cq.data or "").split(":")[-1]
    if locale not in {"ru", "en"}:
        await cq.answer()
        return
    await repo.update_profile(locale=locale)
    await cq.answer(t("language-set"))
    if isinstance(cq.message, Message):
        await cq.message.delete()
        await _render_menu(cq.message, repo, t)
