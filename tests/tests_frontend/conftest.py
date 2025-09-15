import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import allure
import pytest
from playwright.sync_api import Page, sync_playwright

from tests.data.strings import ALL_BROWSERS
from tests.src.data_generators import get_random_string
from tests.src.screens.auth_screen import AuthScreen
from tests.src.screens.register_screen import RegisterScreen

SCREENSHOT_DIR = "screenshots"
DEFAULT_VIEWPORT = {"width": 1440, "height": 900}
TRACE_FILE = "trace.zip"


def pytest_generate_tests(metafunc):
    """Параметризует тесты по браузерам из --browser_type или ALL_BROWSERS.
    Разбивает --browser_type по запятым (например, chromium,webkit),
    либо использует ALL_BROWSERS, если параметр не указан.
    Создает отдельный тест для каждого браузера.
    """
    if "browser_type" in metafunc.fixturenames:
        browser_opt = metafunc.config.getoption("--browser_type")
        browsers = [b.strip() for b in browser_opt.split(",")] if browser_opt else ALL_BROWSERS
        metafunc.parametrize("browser_type", browsers, indirect=True, scope="class")


@pytest.fixture(scope="class")
def browser_type(request):
    """Фикстура для получения типа браузера, используемого в тестах."""
    return request.param


@pytest.fixture(scope="class")
def page(browser_type, request):
    """Фикстура для старта браузера + скриншот при падении"""
    with sync_playwright() as playwright:
        # Инициализация браузера
        browser = getattr(playwright, browser_type).launch(
            headless=request.config.getoption("--headless"))

        context = browser.new_context(permissions=["clipboard-read"], ignore_https_errors=True,
                                      viewport=DEFAULT_VIEWPORT)
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        browser_page = context.new_page()
        browser_page.wait_for_load_state("load")
        allure.dynamic.label("browser", browser_type)
        allure.dynamic.parameter("browser_type", browser_type)

        yield browser_page
        if hasattr(pytest, "test_failed") and pytest.test_failed:
            test_name = getattr(pytest, "current_test_name", "unknown_test")
            save_screenshot(browser_page, f"{test_name}_{browser_type}")  # делаем скриншот при падении
            browser_page.reload()  # делаем рефреш страницы
        save_trace(context)
        browser_page.close()
        context.close()
        browser.close()


def save_screenshot(browser_page, test_name):
    """Сохраняет скриншот с привязкой к Allure"""
    Path(SCREENSHOT_DIR).mkdir(exist_ok=True)
    timestamp = datetime.datetime.now(ZoneInfo("Europe/Moscow")).strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_name = f"{test_name}_{timestamp}.png"
    screenshot_path = f"{SCREENSHOT_DIR}/{screenshot_name}"
    browser_page.screenshot(path=screenshot_path, full_page=True)
    allure.attach.file(screenshot_path,
                       name=screenshot_name,
                       attachment_type=allure.attachment_type.PNG)


def save_trace(context):
    """Сохраняет трассировку действий"""
    context.tracing.stop(path=TRACE_FILE)
    zip_data = Path(TRACE_FILE).read_bytes()
    allure.attach(zip_data, TRACE_FILE)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    if result.when == "call" and result.failed:
        pytest.test_failed = True
        # Улучшаем форматирование имени теста
        pytest.current_test_name = item.name.replace(" ", "_").replace(".", "_")


@pytest.fixture(scope="class")
def create_account(page: Page) -> dict[str, str]:

    name = f"name_{get_random_string()}"
    psw = "password"
    register_screen = RegisterScreen(page)
    auth_screen = AuthScreen(page)

    auth_screen.goto_with_awaiting(page, auth_screen.url)
    auth_screen.click_register_button()
    register_screen.fill_username(name)
    register_screen.fill_password(psw)
    register_screen.fill_password_submit(psw)
    register_screen.click_register_button()
    register_screen.check_success_register()
    page.reload()
    return {"name": name, "password": psw}


@pytest.fixture(scope="class")
def auth(page: Page, create_account):  # noqa: ARG001
    # page.evaluate('return window.sessionStorage.getItem("id_token")') # noqa: ERA001
    return page.evaluate('() => window.sessionStorage.getItem("id_token")')


@pytest.fixture(scope="class")
def open_auth_screen(page):
    AuthScreen(page).goto_with_awaiting(page, AuthScreen(page).url)
