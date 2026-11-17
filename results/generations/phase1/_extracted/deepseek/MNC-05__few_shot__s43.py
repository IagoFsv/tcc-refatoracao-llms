from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class Service:
    name: str
    container: Dict[str, str] = field(default_factory=dict)

@dataclass
class App:
    containers: List[Service] = field(default_factory=list)
    services: Dict[str, Service] = field(default_factory=dict)

def convertContainersToServices(app: App):
    for container in app.containers:
        app.services[container.name] = container
        del app.services[container.name].name
    del app.containers
    return app


def run(app: App):
    """Converts the containers of app into services. Public entry point of this unit."""
    return convertContainersToServices(app)
