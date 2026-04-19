# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-04-19

### Added
- Initial release.
- `/start` flow with inline-menu for visitors: About, Projects, Experience, Skills, Contacts, CV, Language.
- `/admin` panel (restricted to `ADMIN_ID`) — configure name, headline, bio, photo, CV (PDF), projects, experience, skills, contacts, default locale — all from inside Telegram.
- SQLite + SQLAlchemy 2.x async persistence.
- Fluent-based i18n with Russian and English locales.
- Docker multi-stage build, `docker-compose.yml`.
- Deploy recipes: Railway (`railway.json`), Render (`render.yaml`), Fly.io (`fly.toml`).
- CI: ruff lint + format check, mypy, pytest matrix on Python 3.11 / 3.12 / 3.13, Docker build.
- Release workflow: pushes image to GHCR on `v*.*.*` tags.

[Unreleased]: https://github.com/arsenshahverdyanlavtxa228/tg-bot-portfolio-template/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/arsenshahverdyanlavtxa228/tg-bot-portfolio-template/releases/tag/v0.1.0
