from bot.services.i18n import I18n


def test_discovers_locales(i18n: I18n) -> None:
    assert set(i18n.available) == {"ru", "en"}


def test_default_fallback(i18n: I18n) -> None:
    t = i18n.get("xx")
    assert t.locale == i18n.default_locale


def test_known_keys_render(i18n: I18n) -> None:
    ru = i18n.get("ru")
    en = i18n.get("en")
    assert "Обо мне" in ru("menu-about")
    assert "About" in en("menu-about")


def test_interpolation(i18n: I18n) -> None:
    ru = i18n.get("ru")
    rendered = ru("start-welcome", name="Вася", owner="Петя")
    assert "Вася" in rendered and "Петя" in rendered
