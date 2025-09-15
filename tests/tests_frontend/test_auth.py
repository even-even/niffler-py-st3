import allure
import pytest

from tests.data.filters import INCORRECT_AUTH_PARAMS
from tests.src.screens.auth_screen import AuthScreen


@pytest.mark.usefixtures("open_auth_screen")
def test_login(page, create_account, browser_type) -> None:
    allure.dynamic.title(f"Регистрация аккаунта ({browser_type})")

    auth_screen = AuthScreen(page)
    auth_screen.fill_username(create_account["name"])
    auth_screen.fill_password(create_account["password"])
    auth_screen.click_login_button()
    "Congratulations! You've registered!"


@pytest.mark.usefixtures("open_auth_screen")
@pytest.mark.parametrize("login, password", INCORRECT_AUTH_PARAMS)
def test_unsuccess_login(page, login, password, browser_type) -> None:
    allure.dynamic.title(f"Регистрация аккаунта с некорректными данными {login}-{password} ({browser_type})")

    auth_screen = AuthScreen(page)

    auth_screen.fill_username(login)
    auth_screen.fill_password(password)
    auth_screen.click_login_button()
    auth_screen.check_incorrect_pass_label()
