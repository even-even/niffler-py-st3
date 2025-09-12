from playwright.sync_api import Page, expect

from tests.src.screens.base_screen import BaseScreen


class RegisterScreen(BaseScreen):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page = page

        # Определение локаторов
        self.username_field = page.locator("[name='username']")
        self.password_field = page.locator("[name='password']")
        self.password_submit_field = page.locator("[name='passwordSubmit']")
        self.submit_button = page.locator("[type='submit']")
        self.error_message = page.locator(".form__error")
        self.signin_form = page.locator(".form_sign-in")
        self.success_label = page.locator(".form__paragraph_success")

    def fill_username(self, username):
        self.username_field.fill(username)

    def fill_password(self, password):
        self.password_field.fill(password)

    def fill_password_submit(self, password):
        self.password_submit_field.fill(password)

    def click_register_button(self):
        self.submit_button.click()

    def check_incorrect_pass_label(self, error):
        expect(self.error_message.first).to_have_text(error)

    def check_success_register(self):
        expect(self.success_label).to_be_visible()
