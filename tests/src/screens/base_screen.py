import re

from playwright.sync_api import Page

from tests.src.allure_decorators import Step


class BaseScreen:
    """Базовый класс экрана"""

    def __init__(self, page: Page) -> None:
        self.page = page

    def scroll_page(self) -> None:
        with Step("Пролистнуть до футера страницу"):
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    @staticmethod
    def goto_with_awaiting(page: Page, url: str) -> None:
        # 04.09.2025 TODO: добавить поддержку редиректа
        with Step(f"Перейти по урлу {url}"):
            page.goto(url, wait_until="load")
            page.wait_for_url(re.compile(url), wait_until="load")
