def convertContainerToService(container: dict):
    return {container['name']: {**container, 'name': None}}

def convertContainersToServices(app: dict):
    app['services'] = {name: service for container in app['containers'] for name, service in convertContainerToService(container).items()}
    del app['containers']
    return app


def executar(app):
    """Converte os conteineres de app em servicos. Ponto de entrada publico desta unidade."""
    return convertContainersToServices(app)
