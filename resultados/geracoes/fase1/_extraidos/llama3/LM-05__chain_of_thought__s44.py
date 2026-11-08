def executar(html_atual, html_previsao):
    """Le as duas paginas (clima atual e previsao) e devolve o dicionario. Ponto de entrada publico desta unidade."""
    return parse_weather_to_json(
        BeautifulSoup(html_atual, "html.parser"),
        BeautifulSoup(html_previsao, "html.parser"),
    )
