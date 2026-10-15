"""Conversao da lista de conteineres de um aplicativo em servicos nomeados.

Ponto de entrada publico: executar(app). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""


def convertContainersToServices(app: dict):
    app['services'] = {}
    for container in app['containers']:
        app['services'][container['name']] = container
        del app['services'][container['name']]['name']
    del app['containers']
    return app


def executar(app):
    """Converte os conteineres de app em servicos. Ponto de entrada publico desta unidade."""
    return convertContainersToServices(app)
