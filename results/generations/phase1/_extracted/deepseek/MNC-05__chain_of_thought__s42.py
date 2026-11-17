"""Conversion of an app's container list into named services.

Public entry point: run(app). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""


def decompose_container(container):
    name = container.pop('name')
    return name, container


def convertContainersToServices(app):
    app['services'] = {}
    for container in app['containers']:
        service_name, service = decompose_container(container)
        app['services'][service_name] = service
    del app['containers']
    return app


def run(app):
    """Converts the containers of app into services. Public entry point of this unit."""
    return convertContainersToServices(app)
