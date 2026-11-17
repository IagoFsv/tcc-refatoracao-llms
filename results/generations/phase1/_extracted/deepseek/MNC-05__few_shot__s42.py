"""Conversion of an app's container list into named services.

Public entry point: run(app). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class Service:
    name: str
    properties: Dict = field(default_factory=dict)

@dataclass
class App:
    containers: List[Dict] = field(default_factory=list)
    services: Dict[str, Service] = field(default_factory=dict)

def convertContainersToServices(app: App):
    for container in app.containers:
        app.services[container['name']] = Service(name=container['name'], properties=container)
        del app.services[container['name']].properties['name']
    app.containers = []
    return app


def run(app: App):
    """Converts the containers of app into services. Public entry point of this unit."""
    return convertContainersToServices(app)
