# tg-bot-portfolio-template

[![CI](https://github.com/arsenshahverdyanlavtxa228/tg-bot-portfolio-template/actions/workflows/ci.yml/badge.svg)](https://github.com/arsenshahverdyanlavtxa228/tg-bot-portfolio-template/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-2ea44f)](https://github.com/aiogram/aiogram)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Docker](https://img.shields.io/badge/docker-ready-2496ed.svg?logo=docker&logoColor=white)](Dockerfile)

> A self-hostable Telegram bot that acts as a personal portfolio / business card.
> **Everything is configured from inside Telegram** — fork, deploy, run `/admin`, and fill in your profile.
> No code editing required for end users.

---

## ✨ Features

- 📇 **Portfolio sections** — About, Projects, Experience, Skills, Contacts, downloadable CV (PDF).
- 🛠 **In-bot admin panel** — `/admin` command opens an inline UI to edit everything: name, headline, bio, avatar photo, project cards (with images), experience timeline, skill chips, contact links, CV upload. No YAML, no redeploys.
- 🌐 **Multilingual out of the box** — Russian & English via [Fluent](https://projectfluent.org/). Add a locale = drop a folder.
- 💾 **SQLite persistence** — zero-config on Docker volumes. Swap to Postgres via `DATABASE_URL`.
- 🐳 **Production-ready Docker** — multi-stage build, non-root user, ~90 MB runtime image.
- 🚀 **One-click deploy** to Railway / Render / Fly.io (free tiers).
- ✅ **CI & type-safety** — ruff + mypy `strict` + pytest matrix (3.11, 3.12, 3.13), Docker build, GHCR release on tag.

## 📸 Preview

```
┌──────────────────────────────────────┐
│  👋 Hi, friend!                      │
│                                      │
│  This is the portfolio of Jane Doe.  │
│                                      │
│  [ 👤 About  ] [ 💼 Projects ]       │
│  [ 🧭 Exp.   ] [ 🧠 Skills   ]       │
│  [ 📬 Contact] [ 📄 CV       ]       │
│  [ 🌐 Language              ]        │
└──────────────────────────────────────┘
```

<sub>Add real screenshots / a GIF to `docs/` once your bot is live.</sub>

---

## 🚀 Quick start

### 1. Create a bot & grab your Telegram ID

1. Open [@BotFather](https://t.me/BotFather) → `/newbot` → save the **token**.
2. Open [@userinfobot](https://t.me/userinfobot) → save your numeric **user ID** (this becomes `ADMIN_ID`).

### 2. Pick your deploy target

| Target | Difficulty | Cost | Persistent storage |
|---|---|---|---|
| [Docker (local / VPS)](#-docker-local-or-vps) | ⭐ | free | volume |
| [Railway](#-railway) | ⭐ | free trial → $5/mo | volume |
| [Render](#-render) | ⭐⭐ | free worker | 1 GB disk |
| [Fly.io](#-flyio) | ⭐⭐ | free small VM | volume |

---

### 🐳 Docker (local or VPS)

```bash
git clone https://github.com/arsenshahverdyanlavtxa228/tg-bot-portfolio-template.git
cd tg-bot-portfolio-template
cp .env.example .env          # fill BOT_TOKEN and ADMIN_ID
docker compose up -d --build
docker compose logs -f bot
```

Stop with `docker compose down`. Data persists in `./data/`.

### 🚂 Railway

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/template)

1. Fork this repo to your GitHub.
2. In Railway: **New Project → Deploy from GitHub** → pick the fork.
3. **Variables** → add `BOT_TOKEN` and `ADMIN_ID`.
4. **Settings → Volumes** → mount one at `/app/data` (1 GB is plenty).
5. Deploy. Check logs for `bot.starting`.

### 🎨 Render

1. Fork this repo.
2. On [render.com](https://render.com) → **New → Blueprint** → point at your fork.
3. Render reads `render.yaml` and prompts for `BOT_TOKEN` + `ADMIN_ID`.
4. Click **Apply**. Worker deploys with a 1 GB attached disk.

### 🎈 Fly.io

```bash
fly launch --copy-config --no-deploy   # reuses fly.toml
fly volumes create bot_data --size 1
fly secrets set BOT_TOKEN=xxxxxx ADMIN_ID=123456789
fly deploy
```

---

## ⚙️ Configuration

All settings are environment variables. See [`.env.example`](.env.example).

| Variable | Required | Default | Description |
|---|---|---|---|
| `BOT_TOKEN` | ✅ | — | Token from [@BotFather](https://t.me/BotFather). |
| `ADMIN_ID` | ✅ | — | Your numeric Telegram user ID. Only this user can run `/admin`. |
| `DATABASE_URL` | — | `sqlite+aiosqlite:///./data/bot.db` | Any SQLAlchemy async URL (e.g. Postgres). |
| `MEDIA_DIR` | — | `./media` | Where uploaded files live (currently file IDs are reused via Telegram, so mostly reserved). |
| `DEFAULT_LOCALE` | — | `ru` | `ru` or `en`. Admin can change in-bot anytime. |
| `LOG_LEVEL` | — | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR`. |
| `DROP_PENDING_UPDATES` | — | `false` | Drop stale updates on startup. |

## 🎮 How to use

On first run, launch the bot, send `/start` — you'll see an empty profile. Then:

```
/admin          → opens the admin panel (only visible to ADMIN_ID)
  ├─ Name, Headline, Bio, Photo, CV
  ├─ Projects     ➕ add / 🗑 remove
  ├─ Experience   ➕ add / 🗑 remove
  ├─ Skills       ➕ add (comma-separated) / 🗑 remove
  ├─ Contacts     📧 email, ✈️ Telegram, 🐙 GitHub, 💼 LinkedIn, 🌐 Website, 📞 Phone
  └─ Language     🇷🇺 Русский / 🇬🇧 English
```

Anyone else who opens the bot sees a polished public profile based on what you entered.

---

## 🧑‍💻 Local development

```bash
make dev          # create .venv and install runtime + dev deps
cp .env.example .env     # fill BOT_TOKEN and ADMIN_ID
make run
```

Other useful targets:

```bash
make lint          # ruff check
make fmt           # ruff format + auto-fix
make typecheck     # mypy strict
make test          # pytest
make cov           # tests with HTML coverage
```

### Project layout

```
src/bot/
  __main__.py        entrypoint — wires bot, dispatcher, middlewares
  config.py          pydantic-settings (.env loader)
  handlers/
    admin.py         FSM flows for /admin
    visitor.py       /start + public section viewing
  keyboards/         inline keyboard builders
  states/            FSM state groups
  database/
    models.py        SQLAlchemy 2.x ORM models
    repo.py          repository pattern
    session.py       async engine + session factory
  middlewares/
    db.py            per-update db session + repository
    i18n.py          per-update translator selection
  services/
    i18n.py          Fluent-based translator
  locales/
    ru/main.ftl, en/main.ftl
```

---

## 🌍 Adding a new language

1. Create `src/bot/locales/<lang>/main.ftl` (copy `en/main.ftl` as a starting point).
2. Translate messages. Keep the keys identical.
3. Restart the bot. Admin can pick the new language in `/admin → Language` after extending the keyboard in `keyboards/admin.py`.

---

## 🗺️ Roadmap ideas (for forks)

- Blog-style posts section.
- Public stats dashboard (visitor count, top sections).
- Postgres support verified in CI.
- Inline-query mode (share profile in any chat).
- Dark/light theme packs for emojis.

## 🤝 Contributing

PRs and issues welcome. Before submitting:

1. `make lint fmt typecheck test` all green.
2. Update `CHANGELOG.md` under `[Unreleased]`.

## 📄 License

[MIT](LICENSE) — do whatever, just keep the notice.
