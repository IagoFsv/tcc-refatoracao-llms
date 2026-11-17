"""Conversion of an app's container list into named services.

Public entry point: run(app). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

def extract_services_from_containers(containers):
    services = {}
    for container in containers:
        services[container['name']] = container.copy()
        del services[container['name']]['name']
    return services


def convertContainersToServices(app: dict):
    app['services'] = extract_services_from_containers(app['containers'])
    del app['containers']
    return app


def run(app):
    """Converts the containers of app into services. Public entry point of this unit."""
    return convertContainersToServices(app)
