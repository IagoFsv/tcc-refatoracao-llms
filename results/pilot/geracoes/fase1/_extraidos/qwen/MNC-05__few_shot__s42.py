def convertContainersToServices(app: dict):
    app['services'] = {container['name']: container for container in app['containers']}
    app['services'] = {name: {**service, 'name': None} for name, service in app['services'].items()}
    del app['containers']
    return app

def executar(app):
    return convertContainersToServices(app)
