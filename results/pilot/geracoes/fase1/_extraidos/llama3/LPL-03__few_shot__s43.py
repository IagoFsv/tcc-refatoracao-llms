from dataclasses import dataclass, asdict

@dataclass
class Texto:
    valor: str

@dataclass
class Quadro:
    textos: tuple
    poses_elevated: tuple
    width_rectangle: int
    height_reference: int

@dataclass
class Relogio:
    ticks: list

class _Tela:
    """Guarda os quadros em vez de desenhar."""

    def __init__(self):
        self.quadros = []

    def append(self, quadro: Quadro):
        self.quadros.append(quadro)

class _Relogio:
    """Guarda a taxa de cada tick em vez de esperar."""

    def __init__(self):
        self.ticks = []

    def tick(self, framerate):
        self.ticks.append(framerate)

def draw_array(display: _Tela, textos: tuple, width_rectangle: int, height_reference: int, poses_elevated=()):
    display.append(Quadro(textos, poses_elevated, width_rectangle, height_reference))

def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]

def compare_elements(display: _Tela, arrTexts: tuple, *args):
    width_reference, height_reference, arr, i, j = args
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, width_reference, height_reference, [i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        return False
    return True

def simulate_heapsort(arr, arrTexts, display: _Tela, width_reference: int, height_reference: int):
    def heapify(arr, arrTexts, display, width_reference, height_reference, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and compare_elements(
            display, arrTexts, width_reference, height_reference, arr, largest, l
        ):
            largest = l
        if r < n and compare_elements(
            display, arrTexts, width_reference, height_reference, arr, largest, r
        ):
            largest = r
        if largest != i:
            compare_elements(
                display, arrTexts, width_reference, height_reference, arr, i, largest
            )
            swap_elements(arr, arrTexts, i, largest)
            heapify(
                arr, arrTexts, display, width_reference, height_reference, n, largest
            )

    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, arrTexts, display, width_reference, height_reference, n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(arr, arrTexts, i, 0)
        heapify(arr, arrTexts, display, width_reference, height_reference, i, 0)
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = tuple(_Texto(str(x)) for x in arr)
    tela = _Tela()
    clock.ticks.clear()
    simulate_heapsort(arr, textos, tela, 40, 100)
    return arr, tela.quadros, list(clock.ticks)
