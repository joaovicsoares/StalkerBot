from processa_dados import ProcessaDados
from config import Config
from stalker_bot import StalkerBot
from notification_service import NotificationService




def main():
    notificacao = NotificationService(Config.DISCORD_WEBHOOK_URL)
    notificacao.enviar_notificacao("Execução iniciada", "coletando seguidores", "info")
    processaDados = ProcessaDados()
    bot = StalkerBot(Config.ACCOUNT, Config.PASSWORD)
    bot.start()
    bot.login()
    seguindo = bot.BuscaSeguindo(Config.PROFILE)
    seguidores = bot.BuscaSeguidores(Config.PROFILE)
    for seguidor in seguidores:
        print (seguidor["username"])

    seguidoresAntigos = processaDados.recuperaXls(Config.PROFILE)

    seguidoresDiferentes = processaDados.comparaSeguidores(seguidoresAntigos, seguidores)

    processaDados.salvaXls(seguidores, Config.PROFILE)

    notificacao.enviar_notificacao("fim execução", f"Total capturado via API: {len(seguidores)}", "success")
    notificacao.enviar_notificacao("fim execução", f"novos seguidores:{seguidoresDiferentes['novos_seguidores']}", "success")
    notificacao.enviar_notificacao("fim execução", f"parou de seguir:{seguidoresDiferentes['deixaram_de_seguir']}", "success")

    print(f"\nTotal capturado via API: {len(seguidores)}")
    print(f"\nnovos seguidores:{seguidoresDiferentes['novos_seguidores']}")
    print(f"\nparou de seguir:{seguidoresDiferentes['deixaram_de_seguir']}")



if __name__ == "__main__":
    main()
