from dataclasses import dataclass, asdict

class _Texto:
    """Texto ja renderizado de um elemento."""

    def __init__(self, valor):
        self.valor = valor


class _Tela:
    """Guarda os quadros em vez de desenhar."""

    def __init__(self):
        self.quadros = []


class _Relogio:
    """Guarda a taxa de cada tick em vez de esperar."""

    def __init__(self):
        self.ticks = []

    def tick(self, framerate):
        self.ticks.append(framerate)


class _Animacao:
    """Guarda os parâmetros da animação."""

    def __init__(self, valores, width_rectangle, height_reference):
        self.valores = valores
        self.width_rectangle = width_rectangle
        self.height_reference = height_reference


def executar(animacao: _Animacao):
    """Ordena uma copia de valores, animando cada passo. Ponto de entrada publico.

    Devolve (lista ordenada, quadros desenhados, taxas dos ticks do relogio).
    Cada quadro e (textos, posicoes destacadas, largura, altura).
    """
    arr = list(animacao.valores)
    textos = tuple(_Texto(str(x)) for x in arr)
    tela = _Tela()
    clock = _Relogio()
    clock.ticks.clear()
    simulate_heapsort(arr, textos, tela, animacao.width_rectangle, animacao.height_reference)
    return arr, tela.quadros, list(clock.ticks)
