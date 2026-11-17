"""Conversion of an app's container list into named services.

Public entry point: run(app). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

from typing import Dict, List

class Container:
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.__dict__.update(kwargs)

class Service:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def convertContainersToServices(app: Dict[str, any]):
    app['services'] = {}
    for container_data in app['containers']:
        container = Container(**container_data)
        service = Service(**container_data)
        del service.name
        app['services'][container.name] = service
    del app['containers']
    return app


def run(app):
    """Converts the containers of app into services. Public entry point of this unit."""
    return convertContainersToServices(app)
