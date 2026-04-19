## Greeting / menu
start-welcome =
    👋 Привет, { $name }!

    Это визитка { $owner }.
    Выбери раздел — справа всё самое интересное.
start-welcome-empty =
    👋 Привет!

    Этот бот — портфолио. Владелец ещё не заполнил профиль.
    Зайди позже или напиши напрямую.

menu-about = 👤 Обо мне
menu-projects = 💼 Проекты
menu-experience = 🧭 Опыт
menu-skills = 🧠 Навыки
menu-contacts = 📬 Контакты
menu-cv = 📄 Скачать CV
menu-language = 🌐 Язык

back = ⬅️ Назад
cancel = ✖️ Отмена
done = ✅ Готово
delete = 🗑 Удалить
edit = ✏️ Редактировать
add = ➕ Добавить
skip = ⏭ Пропустить

## Sections
about-empty = Раздел «Обо мне» ещё не заполнен.
projects-empty = Проекты ещё не добавлены.
experience-empty = Опыт работы ещё не добавлен.
skills-empty = Навыки ещё не добавлены.
contacts-empty = Контакты ещё не указаны.
cv-empty = CV ещё не загружен.

about-header = 👤 <b>{ $name }</b>
about-headline = <i>{ $headline }</i>
project-title = <b>{ $title }</b>
project-link = 🔗 <a href="{ $url }">Открыть</a>
experience-title = <b>{ $role }</b> — { $company }
experience-period = <i>{ $period }</i>
skills-header = 🧠 <b>Навыки</b>

## Admin
admin-welcome =
    🛠 <b>Панель администратора</b>

    Настрой здесь то, что увидят посетители бота.
admin-not-allowed = ⛔ Эта команда доступна только владельцу бота.

admin-set-name = Имя
admin-set-headline = Должность
admin-set-bio = О себе
admin-set-photo = Фото
admin-set-cv = CV (PDF)
admin-projects = Проекты
admin-experience = Опыт
admin-skills = Навыки
admin-contacts = Контакты
admin-language = Язык по умолчанию

prompt-name = Введи имя (оно будет в шапке):
prompt-headline = Введи должность/роль одной строкой:
prompt-bio = Расскажи о себе. Любой текст, можно с переносами.
prompt-photo = Пришли фото — оно станет аватаром профиля.
prompt-cv = Пришли PDF-файл с CV.
prompt-project-title = Название проекта:
prompt-project-description = Описание проекта:
prompt-project-url = Ссылка на проект (или «-» чтобы пропустить):
prompt-project-photo = Пришли картинку проекта (или нажми «Пропустить»).
prompt-experience-company = Компания:
prompt-experience-role = Должность:
prompt-experience-period = Период (например, «2022 — настоящее время»):
prompt-experience-description = Описание опыта (или «-»):
prompt-skill = Введи навык (можно через запятую — добавлю сразу несколько):
prompt-contact-value = Введи значение для «{ $kind }»:

confirm-saved = ✅ Сохранено.
confirm-deleted = 🗑 Удалено.
confirm-cleared = 🧹 Очищено.
error-invalid = ⚠️ Не понял. Попробуй ещё раз или нажми «Отмена».
error-pdf-only = ⚠️ Нужен PDF-файл.
error-photo-only = ⚠️ Нужно фото.

## Misc
language-set = 🌐 Язык переключён.
language-ru = 🇷🇺 Русский
language-en = 🇬🇧 English
