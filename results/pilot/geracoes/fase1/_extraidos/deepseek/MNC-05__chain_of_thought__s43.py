def create_services_dict(app: dict):
    app['services'] = {}
    return app

def copy_and_remove_name(container, app):
    app['services'][container['name']] = container
    del app['services'][container['name']]['name']
    return app

def remove_containers(app):
    del app['containers']
    return app

def convertContainersToServices(app: dict):
    app = create_services_dict(app)
    for container in app['containers']:
        app = copy_and_remove_name(container, app)
    app = remove_containers(app)
    return app

def executar(app):
    """Converte os conteineres de app em servicos. Ponto de entrada publico desta unidade."""
    return convertContainersToServices(app)
