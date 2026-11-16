from dataclasses import dataclass, asdict

@dataclass
class Texto:
    valor: str

@dataclass
class Tela:
    quadros: list

@dataclass
class Relogio:
    ticks: list

@dataclass
class Params:
    display: Tela
    arrTexts: list
    width_reference: int
    height_reference: int

FREQUENCY_CLOCK = 3

clock = Relogio([])

def draw_array(params: Params):
    textos = tuple(texto.valor for texto in params.arrTexts)
    params.display.quadros.append((textos, tuple(poses_elevated), params.width_reference, params.height_reference))

def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]

def compare_elements(params: Params, arr, i, j):
    draw_array(params)
    clock.ticks.append(FREQUENCY_CLOCK)
    draw_array(params)
    clock.ticks.append(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        return False
    return True

def heapify(params: Params, arr, arrTexts, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and compare_elements(params, arr, largest, l):
        largest = l
    if r < n and compare_elements(params, arr, largest, r):
        largest = r
    if largest != i:
        compare_elements(params, arr, i, largest)
        swap_elements(arr, arrTexts, i, largest)
        heapify(params, arr, arrTexts, n, largest)

def simulate_heapsort(arr, arrTexts, display, width_reference, height_reference):
    arr = list(arr)
    arrTexts = [_Texto(str(x)) for x in arr]
    display = Tela([])
    clock.ticks.clear()
    params = Params(display, arrTexts, width_reference, height_reference)
    n = len(arr)
    for i in range(n, -1, -1):
        heapify(params, arr, arrTexts, n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(arr, arrTexts, i, 0)
        heapify(params, arr, arrTexts, i, 0)
    draw_array(params)
    clock.ticks.append(FREQUENCY_CLOCK)
    return arr, display.quadros, list(clock.ticks)

def executar(valores):
    return simulate_heapsort(valores, [], Tela([]), 40, 100)
