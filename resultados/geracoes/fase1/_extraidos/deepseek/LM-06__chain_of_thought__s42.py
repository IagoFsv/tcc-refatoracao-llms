"""Resposta de linha de comando com o clima atual e a previsao.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a,  %d-%b-%y")


def format_weather_data(data, city: str, country_code: str) -> str:
    """Format the weather data to CLI response."""
    # código formatado para CLI aqui


def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    start_time = datetime.now()
    fmt_cli_resp = format_weather_data(dados, cidade, codigo_pais)
    return fmt_cli_resp


def format_weather_data(data, city: str, country_code: str) -> str:
    """Format the weather data to CLI response."""
    # código formatado para CLI aqui
