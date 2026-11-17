"""Conversion of an app's container list into named services.

Public entry point: run(app). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""


def remove_name_from_container(container: dict):
    """Removes the name key from the container and returns the rest of the container."""
    del container['name']
    return container


def convert_containers_to_services(app: dict):
    """Converts the containers of app into services."""
    app['services'] = {}
    for container in app['containers']:
        app['services'][container['name']] = remove_name_from_container(container)
    del app['containers']
    return app


def run(app):
    """Converts the containers of app into services. Public entry point of this unit."""
    return convert_containers_to_services(app)
