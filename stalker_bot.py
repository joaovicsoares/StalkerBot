from playwright.sync_api import sync_playwright
from followers_service import FollowersService
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

    def _confirmaLogin(self):
        confirmar = True
        while confirmar:
            confirmar = False
            continuar = self.page.locator("div[role='button'][aria-label='Continuar']")
            if continuar.count() > 0:
                confirmar = True
                continuar.click()
                self.page.locator("input[type='password'][name='pass']").fill(self.password)
                self.page.wait_for_timeout(random.randint(1000,5000))
                self.page.get_by_text("Entrar").click()
                self.page.wait_for_timeout(8000)

    def login(self):
        self.page.goto("https://www.instagram.com/")
        self.page.wait_for_timeout(random.randint(3000,6000))
        self.page.locator("input[type='text'][name='email']").fill(self.account)
        self.page.wait_for_timeout(random.randint(1000,5000))
        self.page.locator("input[type='password'][name='pass']").fill(self.password)
        self.page.wait_for_timeout(random.randint(1000,5000))
        self.page.get_by_role("button", name="Entrar", exact=True).click()
        self.page.wait_for_timeout(8000)
        self._confirmaLogin()

    def BuscaSeguidores(self, profile):
        followers_service = FollowersService(self.page)
        followers_service.inicia_coleta()
        self.page.goto(f"https://www.instagram.com/{profile}")
        self.page.wait_for_timeout(5000)
        self.page.locator(f"a[href='/{profile}/followers/']").click()
        self.page.wait_for_timeout(5000)
        modal = self.page.locator("div[role='dialog']")
        divScroll = modal.locator(":scope > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3)")
        last_height = 0
        while True:
            divScroll.evaluate("(el) => el.scrollTop = el.scrollHeight")
            self.page.wait_for_timeout(random.randint(2000,5000))
            height = divScroll.evaluate("(el) => el.scrollHeight")
            if height == last_height:
                break
            last_height = height
        return followers_service.get_seguidores()

    def stop(self):
        self.browser.close()
        self.playwright.stop()

    