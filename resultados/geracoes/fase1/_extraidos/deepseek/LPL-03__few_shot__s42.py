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
    width_reference: int
    height_reference: int
    arr: list
    i: int
    j: int

clock = Relogio([])

def draw_array(display, arrTexts, width_rectangle, height_reference, poses_elevated=()):
    textos = tuple(texto.valor for texto in arrTexts)
    display.quadros.append((textos, tuple(poses_elevated), width_rectangle, height_reference))

def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]

def compare_elements(display, arrTexts, params: Params):
    draw_array(display, arrTexts, params.width_reference, params.height_reference)
    clock.ticks.append(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, params.width_reference, params.height_reference, [params.i, params.j])
    clock.ticks.append(FREQUENCY_CLOCK)
    if (arr[params.i] > arr[params.j] and params.i < params.j) or (arr[params.i] < arr[params.j] and params.i > params.j):
        return False
    return True

def simulate_heapsort(arr, arrTexts, display, width_reference, height_reference):
    def heapify(arr, arrTexts, display, width_reference, height_reference, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and compare_elements(display, arrTexts, Params(width_reference, height_reference, arr, largest, l)):
            largest = l
        if r < n and compare_elements(display, arrTexts, Params(width_reference, height_reference, arr, largest, r)):
            largest = r
        if largest != i:
            compare_elements(display, arrTexts, Params(width_reference, height_reference, arr, i, largest))
            swap_elements(arr, arrTexts, i, largest)
            heapify(arr, arrTexts, display, width_reference, height_reference, n, largest)

    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, arrTexts, display, width_reference, height_reference, n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(arr, arrTexts, i, 0)
        heapify(arr, arrTexts, display, width_reference, height_reference, i, 0)
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.ticks.append(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = Tela([])
    clock.ticks.clear()
    simulate_heapsort(arr, textos, tela, 40, 100)
    return arr, tela.quadros, list(clock.ticks)
