import os
import json
import random
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

PROFILE = os.getenv("PROFILE")
ACCOUNT = os.getenv("ACCOUNT")
PASSWORD = os.getenv("PASSWORD")


def main():
    seguidores = []
    next_max_id = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        def handle_response(response):
            nonlocal seguidores, next_max_id

            if "friendships" in response.url and "followers" in response.url:
                try:
                    data = response.json()

                    users = data.get("users", [])
                    seguidores.extend(users)

                    next_max_id = data.get("next_max_id")
                    print(f"Recebidos {len(users)} seguidores")

                except Exception:
                    pass

        def Login():
            page.goto("https://www.instagram.com/")
            page.wait_for_timeout(random.randint(3000,6000))
            page.locator("input[type='text'][name='email']").fill(ACCOUNT)
            page.wait_for_timeout(random.randint(1000,5000))
            page.locator("input[type='password'][name='pass']").fill(PASSWORD)
            page.wait_for_timeout(random.randint(1000,5000))
            input()
            page.get_by_role("button", name="Entrar", exact=True).click()

            page.wait_for_timeout(8000)

        page.on("response", handle_response)
        Login()

        page.goto(f"https://www.instagram.com/{PROFILE}")
        page.wait_for_timeout(5000)

        page.locator(f"a[href='/{PROFILE}/followers/']").click()
        page.wait_for_timeout(5000)

       
        modal = page.locator("div[role='dialog']")

        last_height = 0

        while True:
            modal.evaluate("(el) => el.scrollTop = el.scrollHeight")
            page.wait_for_timeout(3000)

            height = modal.evaluate("(el) => el.scrollHeight")

            if height == last_height:
                break

            last_height = height

        print(f"\nTotal capturado via API: {len(seguidores)}")

        
        if next_max_id:
            user_id = seguidores[0]["pk"] if seguidores else None

        input("Pressione ENTER para sair...")

        browser.close()


if __name__ == "__main__":
    main()
