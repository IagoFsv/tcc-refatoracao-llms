def executar(texto, escolhas):
    """Resume texto; devolve o resumo e os pedidos feitos. Ponto de entrada publico desta unidade."""
    Request.pedidos = []
    resumo = summarize(texto, escolhas)
    return resumo, Request.pedidos
