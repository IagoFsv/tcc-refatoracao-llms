def convertContainersToServices(app: dict):
    services = {}
    for container in app['containers']:
        container_copy = container.copy()
        container_name = container_copy.pop('name')
        services[container_name] = container_copy
    app['services'] = services
    del app['containers']
    return app


def executar(app):
    """Converte os conteineres de app em servicos. Ponto de entrada publico desta unidade."""
    return convertContainersToServices(app)
