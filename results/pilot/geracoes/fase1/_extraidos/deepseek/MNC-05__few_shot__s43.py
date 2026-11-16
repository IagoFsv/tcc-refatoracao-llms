"""Conversao da lista de conteineres de um aplicativo em servicos nomeados.

Ponto de entrada publico: executar(app). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""


def convertContainersToServices(app: dict):
    app['services'] = {}
    for container in app['containers']:
        service_name = container.pop('name')
        app['services'][service_name] = container
    app.pop('containers')
    return app


def executar(app):
    """Converte os conteineres de app em servicos. Ponto de entrada publico desta unidade."""
    return convertContainersToServices(app)
