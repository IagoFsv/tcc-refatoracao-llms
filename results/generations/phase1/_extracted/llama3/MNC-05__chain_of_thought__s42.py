"""Conversion of an app's container list into named services.

Public entry point: run(app). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""


def convertContainersToServices(app: dict):
    services = {}
    for container in app['containers']:
        services[container['name']] = container
        del services[container['name']]['name']
    app['services'] = services
    del app['containers']
    return app


def run(app):
    """Converts the containers of app into services. Public entry point of this unit."""
    return convertContainersToServices(app)
