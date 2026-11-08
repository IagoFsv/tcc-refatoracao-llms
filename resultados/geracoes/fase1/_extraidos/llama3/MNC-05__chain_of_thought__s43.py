def convertContainersToServices(app: dict):
    services = {}
    for container in app['containers']:
        services[container['name']] = container.copy()
        del services[container['name']]['name']
    del app['containers']
    app['services'] = services
    return app

def executar(app):
    """Converte os conteineres de app em servicos. Ponto de entrada publico desta unidade."""
    return convertContainersToServices(app)
