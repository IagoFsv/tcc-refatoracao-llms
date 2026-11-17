"""Conversion of an app's container list into named services.

Public entry point: run(app). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

from typing import Dict, List

@dataclass
class Container:
    name: str
    # Add other fields as needed

@dataclass
class App:
    containers: List[Container]
    services: Dict[str, Container] = field(default_factory=dict)

def convertContainersToServices(app: App) -> App:
    app.services = {container.name: container for container in app.containers}
    return app


def run(app: App) -> App:
    """Converts the containers of app into services. Public entry point of this unit."""
    return convertContainersToServices(app)
