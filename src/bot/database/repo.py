from collections.abc import Sequence

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Contact, Experience, Profile, Project, Skill, VisitorLog


class Repository:
    """Thin data-access layer. One instance per request, holds a session."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ---------- Profile ----------

    async def get_profile(self) -> Profile:
        result = await self.session.execute(select(Profile).limit(1))
        profile = result.scalar_one_or_none()
        if profile is None:
            profile = Profile()
            self.session.add(profile)
            await self.session.flush()
        return profile

    async def update_profile(self, **fields: object) -> Profile:
        profile = await self.get_profile()
        for key, value in fields.items():
            setattr(profile, key, value)
        await self.session.flush()
        return profile

    # ---------- Projects ----------

    async def list_projects(self) -> Sequence[Project]:
        result = await self.session.execute(
            select(Project).order_by(Project.position, Project.created_at)
        )
        return result.scalars().all()

    async def get_project(self, project_id: int) -> Project | None:
        return await self.session.get(Project, project_id)

    async def add_project(
        self,
        *,
        title: str,
        description: str,
        url: str | None = None,
        photo_file_id: str | None = None,
    ) -> Project:
        next_pos = await self._next_position(Project)
        project = Project(
            title=title,
            description=description,
            url=url,
            photo_file_id=photo_file_id,
            position=next_pos,
        )
        self.session.add(project)
        await self.session.flush()
        return project

    async def delete_project(self, project_id: int) -> None:
        await self.session.execute(delete(Project).where(Project.id == project_id))

    # ---------- Experience ----------

    async def list_experiences(self) -> Sequence[Experience]:
        result = await self.session.execute(
            select(Experience).order_by(Experience.position, Experience.created_at)
        )
        return result.scalars().all()

    async def add_experience(
        self,
        *,
        company: str,
        role: str,
        period: str,
        description: str | None = None,
    ) -> Experience:
        next_pos = await self._next_position(Experience)
        experience = Experience(
            company=company,
            role=role,
            period=period,
            description=description,
            position=next_pos,
        )
        self.session.add(experience)
        await self.session.flush()
        return experience

    async def delete_experience(self, experience_id: int) -> None:
        await self.session.execute(delete(Experience).where(Experience.id == experience_id))

    # ---------- Skills ----------

    async def list_skills(self) -> Sequence[Skill]:
        result = await self.session.execute(select(Skill).order_by(Skill.position, Skill.name))
        return result.scalars().all()

    async def add_skill(self, name: str, category: str | None = None) -> Skill:
        next_pos = await self._next_position(Skill)
        skill = Skill(name=name, category=category, position=next_pos)
        self.session.add(skill)
        await self.session.flush()
        return skill

    async def delete_skill(self, skill_id: int) -> None:
        await self.session.execute(delete(Skill).where(Skill.id == skill_id))

    # ---------- Contacts ----------

    async def list_contacts(self) -> Sequence[Contact]:
        result = await self.session.execute(
            select(Contact).order_by(Contact.position, Contact.kind)
        )
        return result.scalars().all()

    async def set_contact(self, kind: str, value: str) -> Contact:
        result = await self.session.execute(select(Contact).where(Contact.kind == kind))
        contact = result.scalar_one_or_none()
        if contact is None:
            next_pos = await self._next_position(Contact)
            contact = Contact(kind=kind, value=value, position=next_pos)
            self.session.add(contact)
        else:
            await self.session.execute(
                update(Contact).where(Contact.id == contact.id).values(value=value)
            )
        await self.session.flush()
        return contact

    async def delete_contact(self, kind: str) -> None:
        await self.session.execute(delete(Contact).where(Contact.kind == kind))

    # ---------- Visitors ----------

    async def log_visitor(self, tg_user_id: int, tg_username: str | None) -> None:
        result = await self.session.execute(
            select(VisitorLog.id).where(VisitorLog.tg_user_id == tg_user_id).limit(1)
        )
        if result.scalar_one_or_none() is None:
            self.session.add(VisitorLog(tg_user_id=tg_user_id, tg_username=tg_username))

    # ---------- internal ----------

    async def _next_position(self, model: type) -> int:
        result = await self.session.execute(select(func.coalesce(func.max(model.position), -1)))  # type: ignore[attr-defined]
        return int(result.scalar_one()) + 1
