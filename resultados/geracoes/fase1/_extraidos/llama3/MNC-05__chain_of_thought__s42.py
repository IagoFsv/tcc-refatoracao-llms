class Container:
    def __init__(self, name, **kwargs):
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)

class Service:
    def __init__(self, container):
        self.container = container

def convert_containers_to_services(app):
    app.services = {}
    for container in app.containers:
        service = Service(container)
        del service.container.name
        app.services[container.name] = service
    app.containers = []
    return app

def executar(app):
    return convert_containers_to_services(app)
