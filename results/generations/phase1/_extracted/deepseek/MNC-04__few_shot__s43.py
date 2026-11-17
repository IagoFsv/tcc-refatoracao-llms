from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Service:
    env: Dict[str, str] = field(default_factory=dict)
    volumes: List[str] = field(default_factory=list)

@dataclass
class Permissions:
    lnd: Service = Service()
    bitcoind: Service = Service()

permissions = Permissions()

def run(name):
    """Returns the permission of a service. Public entry point of this unit."""
    if name == "lnd":
        return permissions.lnd
    elif name == "bitcoind":
        return permissions.bitcoind
