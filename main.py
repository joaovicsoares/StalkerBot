from processa_dados import ProcessaDados
from config import Config
from stalker_bot import StalkerBot




def main():
    processaDados = ProcessaDados()
    bot = StalkerBot(Config.ACCOUNT, Config.PASSWORD)
    bot.start()
    bot.login()
    seguidores = bot.BuscaSeguidores(Config.PROFILE)
    
    for seguidor in seguidores:
        print (seguidor["username"])

    processaDados.salvaXls(seguidores, Config.PROFILE)

    print(f"\nTotal capturado via API: {len(seguidores)}")

    input("Pressione ENTER para sair...")



if __name__ == "__main__":
    main()
