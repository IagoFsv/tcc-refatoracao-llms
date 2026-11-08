def convertContainersToServices(app: dict):
    app['services'] = {}
    for container in app['containers']:
        service_name = container['name']
        service_details = container.copy()
        del service_details['name']
        app['services'][service_name] = service_details
    del app['containers']
    return app


def executar(app):
    """Converte os conteineres de app em servicos. Ponto de entrada publico desta unidade."""
    return convertContainersToServices(app)
