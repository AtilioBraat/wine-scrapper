import requests
from typing import Optional
import logging


logger = logging.getLogger(__name__)

def send_ntfy_notification(topic: str, title: str, message: str, click_url: Optional[str] = None):
    """
    Envia uma notificação push via ntfy.sh.

    Args:
        topic (str): O nome do tópico ntfy.sh para o qual enviar a notificação.
        title (str): O título da notificação.
        message (str): O corpo da mensagem da notificação.
        click_url (Optional[str]): URL para abrir ao clicar na notificação.
    """
    if not topic:
        logger.warning("Tópico ntfy.sh não configurado. Pulando notificação.")
        return

    try:
        requests.post(
            f"https://ntfy.sh/{topic}",
            data=message.encode('utf-8'),
            headers={
                "Title": title.encode('utf-8'),
                "Click": click_url or "",
                "Priority": "high",  # Prioridade alta para o alerta
                "Tags": "tada"       # Adiciona um emoji de comemoração
            },
            timeout=10
        )
        logger.info(f"Notificação enviada para o tópico '{topic}'.")
    except requests.RequestException as e:
        logger.error(f"Falha ao enviar notificação: {e}", exc_info=True)


if __name__ == "__main__":
    """
    Bloco de execução para testar o envio de notificações diretamente.
    Para executar: python -m scrapper.notifier
    """
    import colorlog
    # Configuração de logging colorida para este teste
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        datefmt="%Y-%m-%d",
        log_colors={'INFO': 'green', 'ERROR': 'red'}
    ))
    # Configura o logger raiz para este teste
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    logger.info("Executando teste de notificação para o tópico ntfy.sh...")

    # Use o tópico que você criou
    test_topic = "wineScrapper-caveNacional-sabado"
    test_title = "Teste do Scrapper de Vinhos 🍷"
    test_message = "Esta é uma mensagem de teste para confirmar que as notificações estão funcionando corretamente."
    test_click_url = "https://cavenacional.com.br/"

    send_ntfy_notification(test_topic, test_title, test_message, test_click_url)
    logger.info("Teste concluído. Verifique seu celular para a notificação.")