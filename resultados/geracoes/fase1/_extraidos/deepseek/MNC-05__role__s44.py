def convertContainersToServices(app: dict):
    app['services'] = {container['name']: container for container in app.get('containers', [])}
    del app['containers']
    return app

def executar(app):
    """Converte os conteineres de app em servicos. Ponto de entrada publico desta unidade."""
    return convertContainersToServices(app)
