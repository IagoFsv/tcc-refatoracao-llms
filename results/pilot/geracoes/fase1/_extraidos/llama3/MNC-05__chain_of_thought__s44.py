def convert_container_to_service(container: dict):
    """Converte um container em um serviço."""
    service = container.copy()
    del service['name']
    return service

def convert_containers_to_services(app: dict):
    """Converte os conteineres de app em servicos."""
    app['services'] = {}
    for container in app['containers']:
        app['services'][container['name']] = convert_container_to_service(container)
    del app['containers']
    return app

def executar(app):
    """Converte os conteineres de app em servicos. Ponto de entrada publico desta unidade."""
    return convert_containers_to_services(app)
