def convertContainersToServices(app: dict):
    app['services'] = {container['name']: container.copy() for container in app['containers']}
    del app['services'][container['name']]['name']
    del app['containers']
    return app


def executar(app):
    return convertContainersToServices(app)
