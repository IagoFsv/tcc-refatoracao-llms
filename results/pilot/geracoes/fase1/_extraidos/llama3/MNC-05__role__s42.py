def convert_containers_to_services(app: dict):
    app_services = {}
    for container in app['containers']:
        app_services[container['name']] = {**container, 'name': None}
    del app['containers']
    app['services'] = app_services
    return app

def executar(app):
    return convert_containers_to_services(app)
