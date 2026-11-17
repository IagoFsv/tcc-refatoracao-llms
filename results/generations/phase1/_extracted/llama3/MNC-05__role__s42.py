"""Conversion of an app's container list into named services.

Public entry point: run(app). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""


def convert_container_to_service(container: dict) -> dict:
    """Convert a container into a service."""
    return {k: v for k, v in container.items() if k != 'name'}


def convert_containers_to_services(app: dict) -> dict:
    """Converts the containers of app into services."""
    app['services'] = {}
    for container in app['containers']:
        app['services'][container['name']] = convert_container_to_service(container)
    del app['containers']
    return app


def run(app: dict) -> dict:
    """Converts the containers of app into services. Public entry point of this unit."""
    return convert_containers_to_services(app)
