from playwright.sync_api import sync_playwright
from followers_service import FollowersService
import random
import re

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
        followersService = FollowersService(self.page)
        followersService.inicia_coleta()
        self.page.goto(f"https://www.instagram.com/{profile}")
        self.page.wait_for_timeout(5000)
        
        totalEsperado = None
        try:
            followersLink = self.page.locator(f"a[href='/{profile}/followers/']")
            
            if followersLink.locator("span").count() > 0:
                followersText = followersLink.locator("span").first.inner_text()
            
            numeros = re.findall(r'\d+', followersText.replace(".", "").replace(",", ""))
            if numeros:
                totalEsperado = int(numeros[0])
                print(f"Total de seguidores no perfil: {totalEsperado}")
        except Exception as e:
            print(f"Não foi possível obter o total de seguidores: {e}")
        
        maxTentativasModal = 10
        tentativaModal = 0
        tentativasSemNovos = 0
        
        while tentativaModal < maxTentativasModal:
            tentativaModal += 1
            seguidoresAntes = len(followersService.get_seguidores())
            print(f"\n=== Abrindo modal - Tentativa {tentativaModal}/{maxTentativasModal} ===")
            print(f"Seguidores únicos até agora: {seguidoresAntes}")
            

            self.page.locator(f"a[href='/{profile}/followers/']").click()
            self.page.wait_for_timeout(5000)
            modal = self.page.locator("div[role='dialog']")
            divScroll = modal.locator(":scope > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3)")
            
            lastHeight = 0
            while True:
                divScroll.evaluate("(el) => el.scrollTop = el.scrollHeight")
                self.page.wait_for_timeout(random.randint(2000,5000))
                height = divScroll.evaluate("(el) => el.scrollHeight")
                if height == lastHeight:
                    self.page.wait_for_timeout(random.randint(5000,10000))
                    divScroll.evaluate("(el) => el.scrollTop = el.scrollHeight")
                    height = divScroll.evaluate("(el) => el.scrollHeight")
                    if height == lastHeight:
                        break
                lastHeight = height
            

            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(random.randint(2000,5000))

            
            seguidoresDepois = len(followersService.get_seguidores())
            novosNestaTentativa = seguidoresDepois - seguidoresAntes
            print(f"Novos seguidores capturados: {novosNestaTentativa}")
            print(f"Total de seguidores únicos: {seguidoresDepois}")
            

            if novosNestaTentativa == 0:
                tentativasSemNovos += 1
            else:
                tentativasSemNovos = 0
            
            if totalEsperado and seguidoresDepois >= totalEsperado:
                print(f"\n✓ Todos os {totalEsperado} seguidores foram capturados!")
                break
            
            if tentativasSemNovos >= 3:
                print(f"\nNenhum seguidor novo nas últimas {tentativasSemNovos} tentativas. Encerrando...")
                break
        
        seguidores = followersService.get_seguidores()
        print(f"\n=== RESULTADO FINAL ===")
        print(f"Total de seguidores únicos capturados: {len(seguidores)}")
        if totalEsperado:
            print(f"Esperado: {totalEsperado} | Capturado: {len(seguidores)} | Faltam: {totalEsperado - len(seguidores)}")
        return seguidores

    def stop(self):
        self.browser.close()
        self.playwright.stop()

    