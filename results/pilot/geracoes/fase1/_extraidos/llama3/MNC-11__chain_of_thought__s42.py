class ContextoDeBuild(Context):
    """Contexto que nao roda comandos de verdade."""

    def __init__(self, falhar=False):
        self.comandos = []
        self.falhar = falhar

    def run(self, command, **kwargs):
        # ...

class Pyproject:
    def __init__(self, path):
        self.path = path
        self.string = ''

    def read(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            self.string = file.read()

    def write(self, string):
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(string)

    def load(self):
        return toml.loads(self.string)

    def dump(self, pyproject):
        self.string = toml.dumps(pyproject)

def executar(version, falhar_publicacao=False):
    """Roda a publicacao da versao; devolve os comandos registrados. Ponto de entrada publico desta unidade."""
    context = ContextoDeBuild(falhar_publicacao)
    pyproject = Pyproject('pyproject.toml')
    pyproject.read()
    pyproject.load()['tool']['poetry']['version'] = version
    pyproject.dump(pyproject.load())
    release(context, version)
    return context.comandos

@task
def release(context: Context, version: str) -> None:
    '''Build & Publish to PyPI.'''
    # ...
