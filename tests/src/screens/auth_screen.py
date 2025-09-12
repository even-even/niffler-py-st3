from playwright.sync_api import Page, expect

from tests.src.screens.base_screen import BaseScreen


class AuthScreen(BaseScreen):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page = page
        self.url = "http://auth.niffler.dc:9000/login"

        self.username_field = page.locator("[name='username']")
        self.password_field = page.locator("[name='password']")
        self.login_button = page.locator("[type='submit']")
        self.register_button = page.locator(".form__register")
        self.error_message = page.locator(".form__error")
        self.sign_in_button = page.locator(".form_sign-in").get_by_text("Sign in")

    def fill_username(self, username):
        self.username_field.fill(username)

    def fill_password(self, password):
        self.password_field.fill(password)

    def click_login_button(self):
        self.login_button.click()

    def click_register_button(self):
        self.register_button.click()

    def check_incorrect_pass_label(self):
        expect(self.error_message).to_have_text("Неверные учетные данные пользователя")
