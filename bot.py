"""
WARNING:

Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
in order to get all the dependencies on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the dependencies.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install --upgrade -r requirements.txt`
- Use the same interpreter as the one used to install the bot (`pip install --upgrade -r requirements.txt`)

Please refer to the documentation for more information at
https://documentation.botcity.dev/tutorials/python-automations/web/
"""

# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *
from dotenv import load_dotenv

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

import os
import random

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.FIREFOX
    # driver = webdriver.Firefox()

    # Uncomment to set the WebDriver path
    bot.driver_path = r"browser_driver\geckodriver.exe"
    load_dotenv()
    profile = os.getenv("PROFILE")
    account = os.getenv("ACCOUNT")
    password = os.getenv("PASSWORD")
 
    def BuscarSeguidores():
        for _ in range(15):
            bot.wait(random.randint(200, 1000))
            bot.tab()

        bot.wait(random.randint(200, 1000))
        bot.enter()
        # element = bot.find_element(selector=f"//a[@role='link' and @href='/{profile}/followers/']", by=By.XPATH)
        # driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # driver.execute_script("arguments[0].click();", element)
        bot.wait(5000)
        container = bot.find_element(selector="//div[@role='dialog']", by=By.XPATH)
        lista = container.find_element(by=By.XPATH, value=".//div[contains(@style, 'display: flex') and contains(@style, 'flex-direction: column')]")

        filhos = lista.find_elements(by=By.XPATH, value=".//a[@role='link']")

        divScroll = container.find_element(by=By.XPATH, value="./div[1]/div[2]/div[1]/div[1]/div[3]")
        while True:
            quantidadeSeguidores = len(filhos)
            bot.scroll_element(divScroll, 100, 1000)
            bot.wait(5000)
            bot.scroll_element(divScroll, 100, 1000)
            bot.wait(5000)

            filhos = lista.find_elements(by=By.XPATH, value=".//a[@role='link']")

            if len(filhos) == quantidadeSeguidores:
                break

        print("teste")
        print(filhos)
        listaSeguidores = []
        anterior = ''
        for filho in filhos:
            if filho.get_attribute('href') != anterior:
                listaSeguidores.append(filho.get_attribute('href'))
                anterior = filho.get_attribute('href')
                print(filho.get_attribute('href'))
        print(len(listaSeguidores))

    def FazerLogin():
        bot.browse(f"https://www.instagram.com/")
        bot.wait(10000)

        bot.type_keys(account)

        bot.tab()
        bot.type_keys(password)

        bot.tab()
        bot.tab()
        bot.enter()

        confirmaLogin = bot.find_element(selector='//span[contains(text(), "Continuar")]', by=By.XPATH)
        if confirmaLogin != None:
            confirmaLogin.click()
            bot.wait(2000)
            bot.type_keys(password)
            bot.tab()
            bot.tab()
            bot.enter()
    

    # bot.tab()
    # bot.wait(random.randint(1500, 5000))
    # bot.tab()
    # bot.wait(random.randint(1500, 5000))
    # bot.enter()

    # for _ in range(3):
    #     bot.wait(random.randint(1500, 5000))
    #     bot.tab()
    
    # bot.wait(random.randint(1500, 5000))
    # bot.enter()
    # bot.wait(random.randint(1500, 5000))
    
    FazerLogin()
    
    bot.wait(10000)
    # element = bot.find_element(selector='//div[@role="button" and contains(text(), "Agora não")]', by=By.XPATH)
    # element.click()

    bot.wait(random.randint(1500, 5000))
    bot.browse(f"https://www.instagram.com/{profile}")

    bot.wait(7000)

    BuscarSeguidores()


    # Implement here your logic...
    ...

    # Wait 3 seconds before closing
    input()
    bot.wait(3000)

    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    bot.stop_browser()

    # Uncomment to mark this task as finished on BotMaestro
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="Task Finished OK.",
    #     total_items=0,
    #     processed_items=0,
    #     failed_items=0
    # )


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
