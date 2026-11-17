"""Conversion of an app's container list into named services.

Public entry point: run(app). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""


def convert_containers_to_services(app: dict):
    app_services = {}
    for container in app['containers']:
        service = {**container}
        del service['name']
        app_services[container['name']] = service
    del app['containers']
    app['services'] = app_services
    return app


def run(app):
    """Converts the containers of app into services. Public entry point of this unit."""
    return convert_containers_to_services(app)
