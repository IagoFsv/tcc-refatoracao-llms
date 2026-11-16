from dataclasses import dataclass

@dataclass
class Container:
    name: str
    services: dict

@dataclass
class Service:
    name: str
    data: dict

def convertContainersToServices(app: dict) -> dict:
    services = {}
    for container in app['containers']:
        service = Service(name=container['name'], data=container['data'])
        services[service.name] = service
        service.data.pop('name')
    app['services'] = services
    del app['containers']
    return app

def executar(app: dict) -> dict:
    return convertContainersToServices(app)
