import allure
import pytest

from tests.data.filters import INCORRECT_AUTH_PARAMS
from tests.src.screens.auth_screen import AuthScreen


@pytest.mark.parametrize("login, password", INCORRECT_AUTH_PARAMS)
def test_unsuccess_login(page, login, password, browser_type) -> None:
    allure.dynamic.title(f"Регистрация аккаунта с некорректными данными {login}-{password} ({browser_type})")

    auth_screen = AuthScreen(page)

    auth_screen.goto_with_awaiting(page, auth_screen.url)
    auth_screen.fill_username(login)
    auth_screen.fill_password(password)
    auth_screen.click_login_button()
    auth_screen.check_incorrect_pass_label()
