def convertContainerToService(container):
    """Converte um container em um serviço."""
    service = container.copy()
    del service['name']
    return service

def removeContainerName(container):
    """Remove a chave 'name' do container."""
    if 'name' in container:
        del container['name']

def convertContainersToServices(app: dict):
    """Converte a lista de containers em servicos."""
    app['services'] = {}
    for container in app['containers']:
        service = convertContainerToService(container)
        app['services'][service['name']] = service
    del app['containers']
    return app

def executar(app):
    """Converte os conteineres de app em servicos. Ponto de entrada publico desta unidade."""
    return convertContainersToServices(app)
