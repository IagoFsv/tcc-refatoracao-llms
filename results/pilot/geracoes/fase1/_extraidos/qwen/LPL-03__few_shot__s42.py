from dataclasses import dataclass, asdict

@dataclass
class Tela:
    quadros: list

@dataclass
class Relogio:
    ticks: list

@dataclass
class Elemento:
    valor: str

@dataclass
class EstadoOrdenacao:
    arr: list
    arrText: list
    display: Tela
    width_rectangle: int
    height_reference: int

FREQUENCY_CLOCK = 3

clock = Relogio()

def draw_array(display, arrTexts, width_rectangle, height_reference, poses_elevated=()):
    textos = tuple(texto.valor for texto in arrTexts)
    display.quadros.append((textos, tuple(poses_elevated), width_rectangle, height_reference))

def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]

def compare_elements(display, arrTexts, estado):
    width_reference, height_reference, arr, i, j = estado.arr[0], estado.arr[1], estado.arr[2], estado.arr[3], estado.arr[4]
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, width_reference, height_reference, [i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        return False
    return True

def simulate_heapsort(estado):
    arr, arrText, display, width_rectangle, height_reference = estado.arr[0], estado.arr[1], estado.arr[2], estado.arr[3], estado.arr[4]
    n = len(arr)
    for i in range(n, -1, -1):
        heapify(estado, n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(arr, arrText, i, 0)
        heapify(estado, i, 0)
    draw_array(display, arrText, width_rectangle, height_reference)
    clock.tick(FREQUENCY_CLOCK)

def heapify(estado, n, i):
    arr, arrText, display, width_rectangle, height_reference = estado.arr[0], estado.arr[1], estado.arr[2], estado.arr[3], estado.arr[4]
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and compare_elements(estado, arrText, estado.arr[3], height_reference, arr, largest, l):
        largest = l
    if r < n and compare_elements(estado, arrText, estado.arr[3], height_reference, arr, largest, r):
        largest = r
    if largest != i:
        compare_elements(estado, arrText, estado.arr[3], height_reference, arr, i, largest)
        swap_elements(arr, arrText, i, largest)
        heapify(estado, n, largest)

def executar(valores):
    arr = list(valores)
    textos = [Elemento(str(x)) for x in arr]
    tela = Tela(quadros=[])
    clock.ticks.clear()
    estado = EstadoOrdenacao(arr=[arr, textos, tela, 40, 100], display=tela, width_rectangle=40, height_reference=100)
    simulate_heapsort(estado)
    return arr, tela.quadros, list(clock.ticks)
