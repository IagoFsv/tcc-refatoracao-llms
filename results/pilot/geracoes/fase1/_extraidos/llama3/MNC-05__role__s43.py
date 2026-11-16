def convert_containers_to_services(app: dict) -> dict:
    services = {}
    for container in app['containers']:
        services[container['name']] = {**container, 'name': None}
    del app['containers']
    app['services'] = services
    return app

def executar(app: dict) -> dict:
    return convert_containers_to_services(app)
