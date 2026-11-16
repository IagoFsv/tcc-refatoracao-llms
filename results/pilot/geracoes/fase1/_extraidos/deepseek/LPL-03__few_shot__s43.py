from dataclasses import dataclass, asdict

@dataclass
class Texto:
    valor: str

@dataclass
class Parametros:
    arr: list
    textos: list
    display: 'Tela'
    width_reference: int
    height_reference: int

@dataclass
class Tela:
    quadros: list

class Relogio:
    def __init__(self):
        self.ticks = []

    def tick(self, framerate):
        self.ticks.append(framerate)


FREQUENCY_CLOCK = 3
clock = Relogio()

def draw_array(parametros: Parametros):
    textos = tuple(texto.valor for texto in parametros.textos)
    parametros.display.quadros.append((textos, tuple(poses_elevated), parametros.width_reference, parametros.height_reference))

def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]

def compare_elements(parametros: Parametros, i, j):
    draw_array(parametros)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(parametros)
    clock.tick(FREQUENCY_CLOCK)
    if (parametros.arr[i] > parametros.arr[j] and i < j) or (parametros.arr[i] < parametros.arr[j] and i > j):
        return False
    return True

def simulate_heapsort(parametros: Parametros):
    def heapify(n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and compare_elements(parametros, largest, l):
            largest = l
        if r < n and compare_elements(parametros, largest, r):
            largest = r
        if largest != i:
            compare_elements(parametros, i, largest)
            swap_elements(parametros.arr, parametros.textos, i, largest)
            heapify(n, largest)

    n = len(parametros.arr)
    for i in range(n, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(parametros.arr, parametros.textos, i, 0)
        heapify(i, 0)
    draw_array(parametros)
    clock.tick(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = [Texto(str(x)) for x in arr]
    tela = Tela()
    clock.ticks.clear()
    simulate_heapsort(Parametros(arr, textos, tela, 40, 100))
    return arr, tela.quadros, list(clock.ticks)
