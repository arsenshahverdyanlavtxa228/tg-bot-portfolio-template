## Greeting / menu
start-welcome =
    👋 Hi, { $name }!

    This is the portfolio of { $owner }.
    Pick a section — all the good stuff is on the right.
start-welcome-empty =
    👋 Hi!

    This bot is a portfolio. The owner hasn't filled it in yet.
    Check back later or reach out directly.

menu-about = 👤 About
menu-projects = 💼 Projects
menu-experience = 🧭 Experience
menu-skills = 🧠 Skills
menu-contacts = 📬 Contacts
menu-cv = 📄 Download CV
menu-language = 🌐 Language

back = ⬅️ Back
cancel = ✖️ Cancel
done = ✅ Done
delete = 🗑 Delete
edit = ✏️ Edit
add = ➕ Add
skip = ⏭ Skip

## Sections
about-empty = The "About" section is empty.
projects-empty = No projects yet.
experience-empty = No experience added yet.
skills-empty = No skills added yet.
contacts-empty = No contacts set yet.
cv-empty = No CV uploaded yet.

about-header = 👤 <b>{ $name }</b>
about-headline = <i>{ $headline }</i>
project-title = <b>{ $title }</b>
project-link = 🔗 <a href="{ $url }">Open</a>
experience-title = <b>{ $role }</b> — { $company }
experience-period = <i>{ $period }</i>
skills-header = 🧠 <b>Skills</b>

## Admin
admin-welcome =
    🛠 <b>Admin panel</b>

    Configure what visitors of this bot will see.
admin-not-allowed = ⛔ This command is only available to the bot owner.

admin-set-name = Name
admin-set-headline = Headline
admin-set-bio = Bio
admin-set-photo = Photo
admin-set-cv = CV (PDF)
admin-projects = Projects
admin-experience = Experience
admin-skills = Skills
admin-contacts = Contacts
admin-language = Default language

prompt-name = Enter your name (will appear at the top of the profile):
prompt-headline = Enter your headline / title in one line:
prompt-bio = Tell visitors about yourself. Any text.
prompt-photo = Send a photo — it will be used as your profile avatar.
prompt-cv = Send a PDF file with your CV.
prompt-project-title = Project title:
prompt-project-description = Project description:
prompt-project-url = Project URL (or "-" to skip):
prompt-project-photo = Send a project image (or press "Skip").
prompt-experience-company = Company:
prompt-experience-role = Role:
prompt-experience-period = Period (e.g., "2022 — present"):
prompt-experience-description = Description (or "-"):
prompt-skill = Enter a skill (comma-separated to add several at once):
prompt-contact-value = Enter the value for "{ $kind }":

confirm-saved = ✅ Saved.
confirm-deleted = 🗑 Deleted.
confirm-cleared = 🧹 Cleared.
error-invalid = ⚠️ Didn't get it. Try again or press "Cancel".
error-pdf-only = ⚠️ PDF file required.
error-photo-only = ⚠️ Photo required.

## Misc
language-set = 🌐 Language switched.
language-ru = 🇷🇺 Русский
language-en = 🇬🇧 English
