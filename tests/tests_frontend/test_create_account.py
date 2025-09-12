import allure
import pytest
from playwright.sync_api import Page

from tests.data.filters import INCORRECT_REGISTER_PARAMS
from tests.src.data_generators import get_random_string
from tests.src.screens.auth_screen import AuthScreen
from tests.src.screens.register_screen import RegisterScreen


def test_create_account(page: Page, browser_type) -> None:
    allure.dynamic.title(f"Регистрация аккаунта ({browser_type})")

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


@pytest.mark.parametrize("name, password, password_submit, error", INCORRECT_REGISTER_PARAMS)
def test_incorrect_create_account(page: Page, name, password, password_submit, error, browser_type) -> None:
    allure.dynamic.title(f"Регистрация аккаунта с некорректными данными {name}-{password} ({browser_type})")

    register_screen = RegisterScreen(page)
    auth_screen = AuthScreen(page)

    auth_screen.goto_with_awaiting(page, auth_screen.url)
    auth_screen.click_register_button()
    register_screen.fill_username(name)
    register_screen.fill_password(password)
    register_screen.fill_password_submit(password_submit)
    register_screen.click_register_button()
    register_screen.check_incorrect_pass_label(error)
