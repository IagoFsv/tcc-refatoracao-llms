from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Container:
    name: str
    data: Dict[str, str] = field(default_factory=dict)

@dataclass
class Service:
    data: Dict[str, str] = field(default_factory=dict)

@dataclass
class App:
    containers: List[Container] = field(default_factory=list)
    services: Dict[str, Service] = field(default_factory=dict)

def convertContainersToServices(app: App):
    for container in app.containers:
        service = Service(data=container.data)
        app.services[container.name] = service
        del app.services[container.name].data['name']
    del app.containers
    return app


def run(app):
    """Converts the containers of app into services. Public entry point of this unit."""
    return convertContainersToServices(app)
