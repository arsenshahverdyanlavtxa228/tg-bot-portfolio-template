import pytest

from bot.database import Repository


@pytest.mark.asyncio
async def test_profile_autocreated(repo: Repository) -> None:
    profile = await repo.get_profile()
    assert profile.id is not None
    assert profile.full_name is None
    assert profile.locale == "ru"


@pytest.mark.asyncio
async def test_update_profile(repo: Repository) -> None:
    await repo.update_profile(full_name="Jane Doe", headline="SWE")
    profile = await repo.get_profile()
    assert profile.full_name == "Jane Doe"
    assert profile.headline == "SWE"


@pytest.mark.asyncio
async def test_projects_order(repo: Repository) -> None:
    for i in range(3):
        await repo.add_project(title=f"P{i}", description="d")
    items = await repo.list_projects()
    assert [p.title for p in items] == ["P0", "P1", "P2"]

    await repo.delete_project(items[1].id)
    remaining = await repo.list_projects()
    assert [p.title for p in remaining] == ["P0", "P2"]


@pytest.mark.asyncio
async def test_contact_upsert(repo: Repository) -> None:
    await repo.set_contact("email", "old@example.com")
    await repo.set_contact("email", "new@example.com")
    contacts = await repo.list_contacts()
    assert len(contacts) == 1
    assert contacts[0].value == "new@example.com"

    await repo.delete_contact("email")
    assert await repo.list_contacts() == []


@pytest.mark.asyncio
async def test_skills_crud(repo: Repository) -> None:
    a = await repo.add_skill("Python")
    await repo.add_skill("Go")
    skills = await repo.list_skills()
    assert {s.name for s in skills} == {"Python", "Go"}
    await repo.delete_skill(a.id)
    skills = await repo.list_skills()
    assert [s.name for s in skills] == ["Go"]


@pytest.mark.asyncio
async def test_visitor_log_deduplicates(repo: Repository) -> None:
    await repo.log_visitor(123, "jane")
    await repo.log_visitor(123, "jane")
    await repo.log_visitor(456, None)
    # Use a fresh query via the session the repo holds.
    from sqlalchemy import func, select

    from bot.database.models import VisitorLog

    result = await repo.session.execute(select(func.count()).select_from(VisitorLog))
    assert result.scalar_one() == 2
