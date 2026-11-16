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
    arr: list
    i: int
    j: int

FREQUENCY_CLOCK = 3

clock = Relogio([])

def draw_array(params: Params):
    textos = tuple(texto.valor for texto in params.arrTexts)
    params.display.quadros.append((textos, tuple([params.i, params.j]), params.width_reference, params.height_reference))

def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]

def compare_elements(params: Params):
    draw_array(params)
    clock.ticks.append(FREQUENCY_CLOCK)
    draw_array(params)
    if (params.arr[params.i] > params.arr[params.j] and params.i < params.j) or (params.arr[params.i] < params.arr[params.j] and params.i > params.j):
        return False
    return True

def compare_and_swap(params: Params):
    swapped = False
    draw_array(params)
    clock.ticks.append(FREQUENCY_CLOCK)
    draw_array(params)
    if (params.arr[params.i] > params.arr[params.j] and params.i < params.j) or (params.arr[params.i] < params.arr[params.j] and params.i > params.j):
        swap_elements(params.arr, params.arrTexts, params.i, params.j)
        draw_array(params)
        clock.ticks.append(FREQUENCY_CLOCK)
        swapped = True
    draw_array(params)
    clock.ticks.append(FREQUENCY_CLOCK)
    return swapped

def simulate_quicksort(arr, arrTexts, display, width_reference, height_reference):
    def partition(params: Params):
        i = params.low  - 1
        for j in range(params.low, params.high):
            if compare_elements(Params(params.display, params.arrTexts, params.width_reference, params.height_reference, params.arr, j, params.high)):
                i += 1
                if i != j:
                    compare_and_swap(Params(params.display, params.arrTexts, params.width_reference, params.height_reference, params.arr, i, j))
        if i + 1 != params.high:
            compare_and_swap(Params(params.display, params.arrTexts, params.width_reference, params.height_reference, params.arr, i + 1, params.high))
        return i + 1

    def quicksort(params: Params):
        if params.low < params.high:
            pi = partition(params)
            quicksort(Params(params.display, params.arrTexts, params.width_reference, params.height_reference, params.arr, params.low, pi  - 1))
            quicksort(Params(params.display, params.arrTexts, params.width_reference, params.height_reference, params.arr, pi + 1, params.high))

    quicksort(Params(display, arrTexts, width_reference, height_reference, arr, 0, len(arr)  - 1))
    draw_array(Params(display, arrTexts, width_reference, height_reference, arr, 0, 0))
    clock.ticks.append(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = Tela([])
    clock.ticks.clear()
    simulate_quicksort(arr, textos, tela, 40, 100)
    return arr, tela.quadros, list(clock.ticks)
