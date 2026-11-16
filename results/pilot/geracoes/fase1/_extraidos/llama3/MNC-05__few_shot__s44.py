from dataclasses import dataclass

@dataclass
class Container:
    name: str

@dataclass
class Service:
    name: str
    containers: List[Container] = field(default_factory=list)

def executar(app):
    """Converte os conteineres de app em servicos. Ponto de entrada publico desta unidade."""
    services = {}
    for container in app['containers']:
        service = Service(name=container['name'])
        service.containers.append(Container(name=container['name']))
        services[container['name']] = service
    del app['containers']
    app['services'] = services
    return app
