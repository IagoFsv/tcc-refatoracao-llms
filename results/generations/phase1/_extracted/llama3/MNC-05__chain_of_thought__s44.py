"""Conversion of an app's container list into named services.

Public entry point: run(app). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""


def convertContainerToService(container: dict):
    """Converts a container into a service."""
    service = container.copy()
    del service['name']
    return service


def convertContainersToServices(app: dict):
    """Converts the containers of app into services."""
    app['services'] = {}
    for container in app['containers']:
        app['services'][container['name']] = convertContainerToService(container)
    del app['containers']
    return app


def run(app):
    """Converts the containers of app into services. Public entry point of this unit."""
    return convertContainersToServices(app)
