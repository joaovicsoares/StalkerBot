from playwright.sync_api import sync_playwright
import random

class StalkerBot:
    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def login(self):
        self.page.goto("https://www.instagram.com/")
        self.page.wait_for_timeout(random.randint(3000,6000))
        self.page.locator("input[type='text'][name='email']").fill(self.account)
        self.page.wait_for_timeout(random.randint(1000,5000))
        self.page.locator("input[type='password'][name='pass']").fill(self.password)
        self.page.wait_for_timeout(random.randint(1000,5000))
        self.page.get_by_role("button", name="Entrar", exact=True).click()
        self.page.wait_for_timeout(8000)
        continuar = self.page.locator("div[role='button'][aria-label='Continuar']")
        if continuar.count() > 0:
            continuar.click()
            self.page.locator("input[type='password'][name='pass']").fill(self.password)
            self.page.wait_for_timeout(random.randint(1000,5000))
            self.page.get_by_text("Entrar").click()
            self.page.wait_for_timeout(8000)