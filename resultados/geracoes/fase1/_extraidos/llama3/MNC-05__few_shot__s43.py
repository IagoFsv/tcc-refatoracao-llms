from dataclasses import dataclass

@dataclass
class Container:
    name: str

def executar(app: dict):
    """Converte os conteineres de app em servicos. Ponto de entrada publico desta unidade."""
    services = {}
    for container in app['containers']:
        service = Container(name=container['name'])
        service_dict = {key: value for key, value in container.items() if key != 'name'}
        services[service.name] = service_dict
    app['services'] = services
    del app['containers']
    return app
