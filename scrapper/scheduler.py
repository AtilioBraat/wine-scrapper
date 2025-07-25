import schedule
import time
import re
from datetime import datetime
from typing import Optional
import logging
import os

from .scraper_core import extrair_dados_degustacoes
from .notifier import send_ntfy_notification

logger = logging.getLogger(__name__)

# --- CONFIGURAÇÃO ---
# Altere estes valores para o seu caso de uso
URL_ALVO = "https://cavenacional.com.br/247-degustacoes-"
# Lê o tópico da variável de ambiente (para o GitHub Actions)
# ou usa um valor padrão (para testes locais).
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "wineScrapper-caveNacional-sabado")
# --------------------

def extrair_data_do_titulo(titulo: str) -> Optional[datetime]:
    """
    Tenta extrair uma data (DD-MM) do início do título e a converte para um objeto datetime.
    """
    # Padrão regex para encontrar datas no formato DD-MM no início da string.
    padrao_data = re.match(r'^(\d{1,2})-(\d{1,2})', titulo)

    if not padrao_data:
        return None

    dia_str, mes_str = padrao_data.groups()
    ano_atual = datetime.now().year

    try:
        # Cria um objeto de data com o ano atual.
        return datetime(year=ano_atual, month=int(mes_str), day=int(dia_str))
    except ValueError:
        # Lida com datas inválidas, como 31-02, etc.
        return None

def executar_scraping():
    """
    Função que será executada diariamente.
    """
    logger.info("Iniciando a rotina de scraping de degustações...")
    lista_de_eventos = extrair_dados_degustacoes(URL_ALVO)

    if not lista_de_eventos:
        logger.warning("Não foi possível extrair a lista de eventos ou nenhum foi encontrado.")
        return

    logger.info(f"Foram encontrados {len(lista_de_eventos)} eventos de degustação:")
    sabado_encontrado = False
    # Nomes dos dias da semana em português para exibição
    dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]

    for i, evento in enumerate(lista_de_eventos, 1):
        data_evento = extrair_data_do_titulo(evento.title)

        if data_evento:
            dia_da_semana_str = dias_semana[data_evento.weekday()]
            logger.debug(f"{i}. {evento.title} - {evento.price} ({dia_da_semana_str})")

            if data_evento.weekday() == 5:  # 5 é Sábado
                logger.info(f"ACHOU! Degustação em um SÁBADO: '{evento.title}'")
                sabado_encontrado = True

                send_ntfy_notification(
                    topic=NTFY_TOPIC,
                    title=f"🍷 {evento.title}",
                    message=f"Preço: {evento.price}",
                    click_url=evento.link
                )
        else:
            logger.debug(f"{i}. {evento.title} - {evento.price} (Data não identificada)")

    if not sabado_encontrado:
        logger.info("Nenhuma degustação encontrada para os próximos sábados.")

def iniciar_agendador():
    # --- PARA TESTE ---
    logger.info("Executando o scraper uma vez para teste...")
    executar_scraping()

    # --- CÓDIGO ORIGINAL (DEIXE COMENTADO DURANTE O TESTE) ---
    # print("Agendador iniciado. A tarefa será executada todos os dias às 08:00.")
    # schedule.every().day.at("08:00").do(executar_scraping)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)