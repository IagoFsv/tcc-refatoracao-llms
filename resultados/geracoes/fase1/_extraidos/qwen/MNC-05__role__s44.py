def convertContainerToService(container: dict):
    service = container.copy()
    del service['name']
    return service


def convertContainersToServices(app: dict):
    app['services'] = {container['name']: convertContainerToService(container) for container in app['containers']}
    del app['containers']
    return app


def executar(app):
    """Converte os conteineres de app em servicos. Ponto de entrada publico desta unidade."""
    return convertContainersToServices(app)
