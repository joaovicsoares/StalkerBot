from processa_dados import ProcessaDados
from config import Config
from stalker_bot import StalkerBot
from notification_service import NotificationService




def main():
    notificacao = NotificationService(Config.DISCORD_WEBHOOK_URL)
    notificacao.notificar_inicio(Config.PROFILE)
    processaDados = ProcessaDados()
    bot = StalkerBot(Config.ACCOUNT, Config.PASSWORD)
    bot.start()
    bot.login()
    seguidores = bot.BuscaSeguidores(Config.PROFILE)
    
    for seguidor in seguidores:
        print (seguidor["username"])

    seguidoresAntigos = processaDados.recuperaXls(Config.PROFILE)

    seguidoresDiferentes = processaDados.comparaSeguidores(seguidoresAntigos, seguidores)

    processaDados.salvaXls(seguidores, Config.PROFILE)

    print(f"\nTotal capturado via API: {len(seguidores)}")
    print(f"\nnovos seguidores:{seguidoresDiferentes['novos_seguidores']}")
    print(f"\nparou de seguir:{seguidoresDiferentes['deixaram_de_seguir']}")

    input("Pressione ENTER para sair...")



if __name__ == "__main__":
    main()
