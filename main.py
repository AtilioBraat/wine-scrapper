import logging
import colorlog
from scrapper.scheduler import executar_tarefa_diaria

def setup_logging():
    """Configura o sistema de logging para a aplicação."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Captura logs a partir do nível DEBUG

    # Evita adicionar handlers duplicados
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = colorlog.StreamHandler()
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d",
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        }
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def run():
    setup_logging()
    executar_tarefa_diaria()

if __name__ == "__main__":
    run()