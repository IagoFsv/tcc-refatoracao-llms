"""Conversion of an app's container list into named services.

Public entry point: run(app). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""


def convert_container_to_service(container: dict) -> dict:
    service = {}
    for key, value in container.items():
        if isinstance(value, dict):
            service[key] = convert_container_to_service(value)
        else:
            service[key] = value
    return service


def convert_containers_to_services(app: dict) -> dict:
    app['services'] = {}
    for container in app['containers']:
        app['services'][container['name']] = convert_container_to_service(container)
        del app['services'][container['name']]['name']
    del app['containers']
    return app


def run(app: dict) -> dict:
    """Converts the containers of app into services. Public entry point of this unit."""
    return convert_containers_to_services(app)
