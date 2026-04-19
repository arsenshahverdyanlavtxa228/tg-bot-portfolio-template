from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from bot.config import Settings
from bot.database import Repository
from bot.keyboards.admin import (
    admin_contacts_kb,
    admin_experience_kb,
    admin_languages_kb,
    admin_menu_kb,
    admin_projects_kb,
    admin_skills_kb,
    cancel_kb,
    skip_cancel_kb,
)
from bot.services.i18n import Translator
from bot.states import (
    AdminBio,
    AdminContact,
    AdminCV,
    AdminExperience,
    AdminHeadline,
    AdminName,
    AdminPhoto,
    AdminProject,
    AdminSkill,
)

router = Router(name="admin")


class AdminFilter:
    """Accept only updates from the configured ADMIN_ID."""

    def __init__(self, admin_id: int) -> None:
        self.admin_id = admin_id

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return bool(event.from_user and event.from_user.id == self.admin_id)


def setup_filters(settings: Settings) -> None:
    admin_filter = AdminFilter(settings.admin_id)
    router.message.filter(admin_filter)
    router.callback_query.filter(admin_filter)


_CANCEL_TEXTS = frozenset({"✖️ Отмена", "✖️ Cancel"})
_SKIP_TEXTS = frozenset({"⏭ Пропустить", "⏭ Skip"})


def _is_cancel(message: Message, t: Translator) -> bool:
    if not message.text:
        return False
    txt = (message.text or "").strip()
    return txt == t("cancel") or txt in _CANCEL_TEXTS


def _is_skip(message: Message, t: Translator) -> bool:
    if not message.text:
        return False
    txt = (message.text or "").strip()
    return txt == t("skip") or txt in _SKIP_TEXTS


async def _show_admin_menu(message: Message, t: Translator) -> None:
    await message.answer(
        t("admin-welcome"),
        reply_markup=admin_menu_kb(t),
        parse_mode=ParseMode.HTML,
    )


async def _cancel(message: Message, state: FSMContext, t: Translator) -> None:
    await state.clear()
    await message.answer(t("confirm-cleared"), reply_markup=ReplyKeyboardRemove())
    await _show_admin_menu(message, t)


# ----------------------- entry points -----------------------


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext, t: Translator) -> None:
    await state.clear()
    await message.answer("🛠", reply_markup=ReplyKeyboardRemove())
    await _show_admin_menu(message, t)


@router.callback_query(F.data == "a:menu")
async def back_admin_menu(cq: CallbackQuery, state: FSMContext, t: Translator) -> None:
    await state.clear()
    if isinstance(cq.message, Message):
        await cq.message.delete()
        await _show_admin_menu(cq.message, t)
    await cq.answer()


# ----------------------- scalar fields -----------------------


@router.callback_query(F.data == "a:set:name")
async def ask_name(cq: CallbackQuery, state: FSMContext, t: Translator) -> None:
    await state.set_state(AdminName.waiting)
    if isinstance(cq.message, Message):
        await cq.message.answer(t("prompt-name"), reply_markup=cancel_kb(t))
    await cq.answer()


@router.message(AdminName.waiting, F.text)
async def save_name(message: Message, state: FSMContext, repo: Repository, t: Translator) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    await repo.update_profile(full_name=(message.text or "").strip())
    await state.clear()
    await message.answer(t("confirm-saved"), reply_markup=ReplyKeyboardRemove())
    await _show_admin_menu(message, t)


@router.callback_query(F.data == "a:set:headline")
async def ask_headline(cq: CallbackQuery, state: FSMContext, t: Translator) -> None:
    await state.set_state(AdminHeadline.waiting)
    if isinstance(cq.message, Message):
        await cq.message.answer(t("prompt-headline"), reply_markup=cancel_kb(t))
    await cq.answer()


@router.message(AdminHeadline.waiting, F.text)
async def save_headline(
    message: Message, state: FSMContext, repo: Repository, t: Translator
) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    await repo.update_profile(headline=(message.text or "").strip())
    await state.clear()
    await message.answer(t("confirm-saved"), reply_markup=ReplyKeyboardRemove())
    await _show_admin_menu(message, t)


@router.callback_query(F.data == "a:set:bio")
async def ask_bio(cq: CallbackQuery, state: FSMContext, t: Translator) -> None:
    await state.set_state(AdminBio.waiting)
    if isinstance(cq.message, Message):
        await cq.message.answer(t("prompt-bio"), reply_markup=cancel_kb(t))
    await cq.answer()


@router.message(AdminBio.waiting, F.text)
async def save_bio(message: Message, state: FSMContext, repo: Repository, t: Translator) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    await repo.update_profile(bio=(message.text or "").strip())
    await state.clear()
    await message.answer(t("confirm-saved"), reply_markup=ReplyKeyboardRemove())
    await _show_admin_menu(message, t)


@router.callback_query(F.data == "a:set:photo")
async def ask_photo(cq: CallbackQuery, state: FSMContext, t: Translator) -> None:
    await state.set_state(AdminPhoto.waiting)
    if isinstance(cq.message, Message):
        await cq.message.answer(t("prompt-photo"), reply_markup=cancel_kb(t))
    await cq.answer()


@router.message(AdminPhoto.waiting, F.photo)
async def save_photo(message: Message, state: FSMContext, repo: Repository, t: Translator) -> None:
    assert message.photo is not None
    await repo.update_profile(photo_file_id=message.photo[-1].file_id)
    await state.clear()
    await message.answer(t("confirm-saved"), reply_markup=ReplyKeyboardRemove())
    await _show_admin_menu(message, t)


@router.message(AdminPhoto.waiting)
async def reject_non_photo(message: Message, state: FSMContext, t: Translator) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    await message.answer(t("error-photo-only"))


@router.callback_query(F.data == "a:set:cv")
async def ask_cv(cq: CallbackQuery, state: FSMContext, t: Translator) -> None:
    await state.set_state(AdminCV.waiting)
    if isinstance(cq.message, Message):
        await cq.message.answer(t("prompt-cv"), reply_markup=cancel_kb(t))
    await cq.answer()


@router.message(AdminCV.waiting, F.document)
async def save_cv(message: Message, state: FSMContext, repo: Repository, t: Translator) -> None:
    doc = message.document
    assert doc is not None
    if (doc.mime_type or "").lower() != "application/pdf":
        await message.answer(t("error-pdf-only"))
        return
    await repo.update_profile(cv_file_id=doc.file_id, cv_file_name=doc.file_name)
    await state.clear()
    await message.answer(t("confirm-saved"), reply_markup=ReplyKeyboardRemove())
    await _show_admin_menu(message, t)


@router.message(AdminCV.waiting)
async def reject_non_pdf(message: Message, state: FSMContext, t: Translator) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    await message.answer(t("error-pdf-only"))


# ----------------------- projects -----------------------


@router.callback_query(F.data == "a:projects")
async def projects_menu(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    projects = await repo.list_projects()
    if isinstance(cq.message, Message):
        await cq.message.edit_text(t("admin-projects"), reply_markup=admin_projects_kb(t, projects))
    await cq.answer()


@router.callback_query(F.data == "a:project:add")
async def add_project_title(cq: CallbackQuery, state: FSMContext, t: Translator) -> None:
    await state.set_state(AdminProject.title)
    if isinstance(cq.message, Message):
        await cq.message.answer(t("prompt-project-title"), reply_markup=cancel_kb(t))
    await cq.answer()


@router.message(AdminProject.title, F.text)
async def add_project_description(message: Message, state: FSMContext, t: Translator) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    await state.update_data(title=(message.text or "").strip())
    await state.set_state(AdminProject.description)
    await message.answer(t("prompt-project-description"))


@router.message(AdminProject.description, F.text)
async def add_project_url(message: Message, state: FSMContext, t: Translator) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    await state.update_data(description=(message.text or "").strip())
    await state.set_state(AdminProject.url)
    await message.answer(t("prompt-project-url"))


@router.message(AdminProject.url, F.text)
async def add_project_photo(message: Message, state: FSMContext, t: Translator) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    url = (message.text or "").strip()
    await state.update_data(url=None if url == "-" else url)
    await state.set_state(AdminProject.photo)
    await message.answer(t("prompt-project-photo"), reply_markup=skip_cancel_kb(t))


@router.message(AdminProject.photo, F.photo)
async def save_project_with_photo(
    message: Message, state: FSMContext, repo: Repository, t: Translator
) -> None:
    data = await state.get_data()
    assert message.photo is not None
    await repo.add_project(
        title=data["title"],
        description=data["description"],
        url=data.get("url"),
        photo_file_id=message.photo[-1].file_id,
    )
    await state.clear()
    await message.answer(t("confirm-saved"), reply_markup=ReplyKeyboardRemove())
    await _show_admin_menu(message, t)


@router.message(AdminProject.photo, F.text)
async def save_project_skip_photo(
    message: Message, state: FSMContext, repo: Repository, t: Translator
) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    if _is_skip(message, t):
        data = await state.get_data()
        await repo.add_project(
            title=data["title"],
            description=data["description"],
            url=data.get("url"),
        )
        await state.clear()
        await message.answer(t("confirm-saved"), reply_markup=ReplyKeyboardRemove())
        await _show_admin_menu(message, t)
    else:
        await message.answer(t("error-invalid"))


@router.callback_query(F.data.startswith("a:project:del:"))
async def delete_project(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    pid = int((cq.data or "").split(":")[-1])
    await repo.delete_project(pid)
    await cq.answer(t("confirm-deleted"))
    projects = await repo.list_projects()
    if isinstance(cq.message, Message):
        await cq.message.edit_reply_markup(reply_markup=admin_projects_kb(t, projects))


# ----------------------- experience -----------------------


@router.callback_query(F.data == "a:experience")
async def experience_menu(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    items = await repo.list_experiences()
    if isinstance(cq.message, Message):
        await cq.message.edit_text(
            t("admin-experience"), reply_markup=admin_experience_kb(t, items)
        )
    await cq.answer()


@router.callback_query(F.data == "a:exp:add")
async def exp_add_company(cq: CallbackQuery, state: FSMContext, t: Translator) -> None:
    await state.set_state(AdminExperience.company)
    if isinstance(cq.message, Message):
        await cq.message.answer(t("prompt-experience-company"), reply_markup=cancel_kb(t))
    await cq.answer()


@router.message(AdminExperience.company, F.text)
async def exp_add_role(message: Message, state: FSMContext, t: Translator) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    await state.update_data(company=(message.text or "").strip())
    await state.set_state(AdminExperience.role)
    await message.answer(t("prompt-experience-role"))


@router.message(AdminExperience.role, F.text)
async def exp_add_period(message: Message, state: FSMContext, t: Translator) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    await state.update_data(role=(message.text or "").strip())
    await state.set_state(AdminExperience.period)
    await message.answer(t("prompt-experience-period"))


@router.message(AdminExperience.period, F.text)
async def exp_add_description(message: Message, state: FSMContext, t: Translator) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    await state.update_data(period=(message.text or "").strip())
    await state.set_state(AdminExperience.description)
    await message.answer(t("prompt-experience-description"))


@router.message(AdminExperience.description, F.text)
async def exp_save(message: Message, state: FSMContext, repo: Repository, t: Translator) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    data = await state.get_data()
    desc = (message.text or "").strip()
    await repo.add_experience(
        company=data["company"],
        role=data["role"],
        period=data["period"],
        description=None if desc == "-" else desc,
    )
    await state.clear()
    await message.answer(t("confirm-saved"), reply_markup=ReplyKeyboardRemove())
    await _show_admin_menu(message, t)


@router.callback_query(F.data.startswith("a:exp:del:"))
async def delete_experience(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    eid = int((cq.data or "").split(":")[-1])
    await repo.delete_experience(eid)
    await cq.answer(t("confirm-deleted"))
    items = await repo.list_experiences()
    if isinstance(cq.message, Message):
        await cq.message.edit_reply_markup(reply_markup=admin_experience_kb(t, items))


# ----------------------- skills -----------------------


@router.callback_query(F.data == "a:skills")
async def skills_menu(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    items = await repo.list_skills()
    if isinstance(cq.message, Message):
        await cq.message.edit_text(t("admin-skills"), reply_markup=admin_skills_kb(t, items))
    await cq.answer()


@router.callback_query(F.data == "a:skill:add")
async def skill_add(cq: CallbackQuery, state: FSMContext, t: Translator) -> None:
    await state.set_state(AdminSkill.waiting)
    if isinstance(cq.message, Message):
        await cq.message.answer(t("prompt-skill"), reply_markup=cancel_kb(t))
    await cq.answer()


@router.message(AdminSkill.waiting, F.text)
async def skill_save(message: Message, state: FSMContext, repo: Repository, t: Translator) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    names = [s.strip() for s in (message.text or "").split(",") if s.strip()]
    for name in names:
        try:
            await repo.add_skill(name)
        except Exception:  # unique constraint — skip duplicates silently
            continue
    await state.clear()
    await message.answer(t("confirm-saved"), reply_markup=ReplyKeyboardRemove())
    await _show_admin_menu(message, t)


@router.callback_query(F.data.startswith("a:skill:del:"))
async def delete_skill(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    sid = int((cq.data or "").split(":")[-1])
    await repo.delete_skill(sid)
    await cq.answer(t("confirm-deleted"))
    items = await repo.list_skills()
    if isinstance(cq.message, Message):
        await cq.message.edit_reply_markup(reply_markup=admin_skills_kb(t, items))


# ----------------------- contacts -----------------------


@router.callback_query(F.data == "a:contacts")
async def contacts_menu(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    contacts = await repo.list_contacts()
    if isinstance(cq.message, Message):
        await cq.message.edit_text(t("admin-contacts"), reply_markup=admin_contacts_kb(t, contacts))
    await cq.answer()


@router.callback_query(F.data.startswith("a:contact:set:"))
async def ask_contact_value(cq: CallbackQuery, state: FSMContext, t: Translator) -> None:
    kind = (cq.data or "").split(":")[-1]
    await state.set_state(AdminContact.value)
    await state.update_data(kind=kind)
    if isinstance(cq.message, Message):
        await cq.message.answer(t("prompt-contact-value", kind=kind), reply_markup=cancel_kb(t))
    await cq.answer()


@router.message(AdminContact.value, F.text)
async def save_contact(
    message: Message, state: FSMContext, repo: Repository, t: Translator
) -> None:
    if _is_cancel(message, t):
        await _cancel(message, state, t)
        return
    data = await state.get_data()
    await repo.set_contact(data["kind"], (message.text or "").strip())
    await state.clear()
    await message.answer(t("confirm-saved"), reply_markup=ReplyKeyboardRemove())
    await _show_admin_menu(message, t)


@router.callback_query(F.data.startswith("a:contact:del:"))
async def delete_contact(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    kind = (cq.data or "").split(":")[-1]
    await repo.delete_contact(kind)
    await cq.answer(t("confirm-deleted"))
    contacts = await repo.list_contacts()
    if isinstance(cq.message, Message):
        await cq.message.edit_reply_markup(reply_markup=admin_contacts_kb(t, contacts))


# ----------------------- language -----------------------


@router.callback_query(F.data == "a:language")
async def language_menu(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    profile = await repo.get_profile()
    if isinstance(cq.message, Message):
        await cq.message.edit_text(
            t("admin-language"), reply_markup=admin_languages_kb(t, profile.locale)
        )
    await cq.answer()


@router.callback_query(F.data.startswith("a:lang:"))
async def set_language(cq: CallbackQuery, repo: Repository, t: Translator) -> None:
    locale = (cq.data or "").split(":")[-1]
    if locale not in {"ru", "en"}:
        await cq.answer()
        return
    await repo.update_profile(locale=locale)
    await cq.answer(t("language-set"))
    if isinstance(cq.message, Message):
        await cq.message.delete()
        await _show_admin_menu(cq.message, t)
