from aiogram.fsm.state import State, StatesGroup


class AdminName(StatesGroup):
    waiting = State()


class AdminHeadline(StatesGroup):
    waiting = State()


class AdminBio(StatesGroup):
    waiting = State()


class AdminPhoto(StatesGroup):
    waiting = State()


class AdminCV(StatesGroup):
    waiting = State()


class AdminProject(StatesGroup):
    title = State()
    description = State()
    url = State()
    photo = State()


class AdminExperience(StatesGroup):
    company = State()
    role = State()
    period = State()
    description = State()


class AdminSkill(StatesGroup):
    waiting = State()


class AdminContact(StatesGroup):
    value = State()
