def convertContainerToService(container: dict):
    """Converte um único container em um serviço."""
    service = container.copy()
    del service['name']
    return service

def convertContainersToServices(app: dict):
    """Converte os conteineres de app em servicos."""
    app['services'] = {}
    for container in app['containers']:
        app['services'][container['name']] = convertContainerToService(container)
    del app['containers']
    return app

def executar(app):
    """Converte os conteineres de app em servicos. Ponto de entrada publico desta unidade."""
    return convertContainersToServices(app)
