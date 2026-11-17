"""Conversion of an app's container list into named services.

Public entry point: run(app). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""


def convertContainersToServices(app: dict):
    services = {}
    for container in app['containers']:
        container_copy = container.copy()
        container_name = container_copy.pop('name')
        services[container_name] = container_copy
    app['services'] = services
    return app


def run(app):
    """Converts the containers of app into services. Public entry point of this unit."""
    return convertContainersToServices(app)
