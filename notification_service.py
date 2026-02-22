import requests
from datetime import datetime

class NotificationService:
    def __init__(self, webhookUrl):
        self.webhookUrl = webhookUrl
    
    def enviar_notificacao(self, titulo, mensagem, cor=None):
        cores = {
        'success': 0x00ff00,  
        'error': 0xff0000,    
        'warning': 0xffaa00,  
        'info': 0x0099ff      
        }

        corHex = cores.get(cor, 0x808080)

        embed = {
        "title": titulo,
        "description": mensagem,
        "color": corHex,
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {"text": "StalkerBot"}
        } 

        payload = {"embeds": [embed]}

        try:
            response = requests.post(self.webhookUrl, json=payload)
            return response.status_code == 204
        except Exception as e:
            print(f"Erro ao enviar notificação: {e}")
            return False

    def notificar_inicio(self, perfil):
        mensagem = f"Iniciando coleta de seguidores do perfil **@{perfil}**"
        self.enviar_notificacao("🚀 Execução Iniciada", mensagem, 'info')

