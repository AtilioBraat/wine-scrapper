import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Degustacao:
    """Estrutura para armazenar os dados de uma degustação."""
    title: str
    price: str
    link: str

def extrair_informacao_do_site(url: str, div_id: str) -> str | None:
    """
    Acessa uma URL, encontra uma div pelo seu ID e retorna o texto contido nela.

    Args:
        url (str): A URL do site a ser acessado.
        div_id (str): O ID da div da qual o texto será extraído.

    Returns:
        str | None: O texto da div se encontrada, caso contrário None.
    """
    logger.info(f"Acessando a URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontra a div pelo ID
        target_div = soup.find('div', id=div_id)
        
        return target_div.get_text(strip=True) if target_div else None
    except requests.RequestException as e:
        logger.error(f"Erro ao acessar o site: {e}", exc_info=True)
        return None

def extrair_dados_degustacoes(url: str) -> Optional[List[Degustacao]]:
    """
    Acessa a página de degustações e extrai o título, preço e link de cada produto.

    Args:
        url (str): A URL da página de degustações.

    Returns:
        Optional[List[Degustacao]]: Uma lista de objetos Degustacao ou None se ocorrer um erro.
    """
    logger.info(f"Acessando a URL para extrair dados: {url}")
    try:
        response = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Seletor para encontrar cada "card" de produto
        product_cards = soup.select("#js-product-list .product-miniature")
        
        eventos = []
        for card in product_cards:
            title_element = card.select_one(".product-description h2 a")
            price_element = card.select_one(".price")

            if title_element:
                link_href = title_element.get('href', '')
                # The 'href' attribute should always be a string. We assert our
                # assumption here to satisfy mypy and catch unexpected cases.
                assert isinstance(link_href, str)

                eventos.append(Degustacao(
                    title=title_element.get_text(strip=True),
                    link=link_href,
                    price=price_element.get_text(strip=True) if price_element else "N/A"
                ))
        return eventos
    except requests.RequestException as e:
        logger.error(f"Erro ao acessar o site: {e}", exc_info=True)
        return None