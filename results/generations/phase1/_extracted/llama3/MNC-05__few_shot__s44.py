"""Conversion of an app's container list into named services.

Public entry point: run(app). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""


class Container:
    def __init__(self, name, **kwargs):
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)

def convert_containers_to_services(app: dict):
    app_services = {}
    for container in app.get('containers', []):
        app_services[container.name] = Container(**container)
        del app_services[container.name].name
    del app.get('containers', None)
    app['services'] = app_services
    return app


def run(app):
    """Converts the containers of app into services. Public entry point of this unit."""
    return convert_containers_to_services(app)
