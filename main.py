
import pandas as pd
from config import Config
from stalker_bot import StalkerBot




def main():
    bot = StalkerBot(Config.ACCOUNT, Config.PASSWORD)
    bot.start()
    bot.login()
    seguidores = bot.BuscaSeguidores()
    
    for seguidor in seguidores:
        print (seguidor["username"])

    df = pd.DataFrame(seguidores, columns=["username"])
    df.to_excel("seguidores.xlsx", index=False)

    print(f"\nTotal capturado via API: {len(seguidores)}")

    input("Pressione ENTER para sair...")



if __name__ == "__main__":
    main()
