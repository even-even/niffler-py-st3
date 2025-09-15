from pytest import Parser  # noqa: PT013


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--browser_type",
        default="chromium",
        help="Тип браузера для запуска тестов фронтенда через запятую (chromium, firefox, webkit)"
        # Список браузеров. Firefox в CI не гоняется
    )

    parser.addoption(
        "--headless",
        action="store_true",
        help="headless (без UI) режим."
    )

    parser.addoption(
        "--mobile_devices",
        default="",
        help="Тип мобильного устройства для запуска тестов фронтенда через запятую ['iPhone 14', 'Galaxy S24']"
    )
