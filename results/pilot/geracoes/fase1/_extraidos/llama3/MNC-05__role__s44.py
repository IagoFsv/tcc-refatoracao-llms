def convert_containers_to_services(app: dict):
    services = {}
    for container in app['containers']:
        services[container['name']] = {k: v for k, v in container.items() if k != 'name'}
    del app['containers']
    app['services'] = services
    return app

def executar(app):
    return convert_containers_to_services(app)
