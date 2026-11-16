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
    clock.ticks.append(3)
    draw_array(display, arrTexts, params.width_reference, params.height_reference, [params.i, params.j])
    clock.ticks.append(3)
    if (params.arr[params.i] > params.arr[params.j] and params.i < params.j) or (params.arr[params.i] < params.arr[params.j] and params.i > params.j):
        return False
    return True

def compare_and_swap(display, arrTexts, params: Params):
    swapped = False
    draw_array(display, arrTexts, params.width_reference, params.height_reference)
    clock.ticks.append(3)
    draw_array(display, arrTexts, params.width_reference, params.height_reference, [params.i, params.j])
    clock.ticks.append(3)
    if (params.arr[params.i] > params.arr[params.j] and params.i < params.j) or (params.arr[params.i] < params.arr[params.j] and params.i > params.j):
        swap_elements(params.arr, arrTexts, params.i, params.j)
        draw_array(display, arrTexts, params.width_reference, params.height_reference, [params.i, params.j])
        clock.ticks.append(3)
        swapped = True
    draw_array(display, arrTexts, params.width_reference, params.height_reference)
    clock.ticks.append(3)
    return swapped

def simulate_quicksort(arr, arrTexts, display, width_reference, height_reference):
    def partition(arr, arrTexts, display, width_reference, height_reference, low, high):
        i = low - 1
        for j in range(low, high):
            params = Params(width_reference, height_reference, arr, j, high)
            if compare_elements(display, arrTexts, params):
                i += 1
                if i != j:
                    compare_and_swap(display, arrTexts, Params(width_reference, height_reference, arr, i, j))
        if i + 1 != high:
            compare_and_swap(display, arrTexts, Params(width_reference, height_reference, arr, i + 1, high))
        return i + 1

    def quicksort(arr, arrTexts, display, width_reference, height_reference, low, high):
        if low < high:
            pi = partition(arr, arrTexts, display, width_reference, height_reference, low, high)
            quicksort(arr, arrTexts, display, width_reference, height_reference, low, pi - 1)
            quicksort(arr, arrTexts, display, width_reference, height_reference, pi + 1, high)

    quicksort(arr, arrTexts, display, width_reference, height_reference, 0, len(arr) - 1)
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.ticks.append(3)

def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = Tela([])
    clock.ticks.clear()
    simulate_quicksort(arr, textos, tela, 40, 100)
    return arr, tela.quadros, list(clock.ticks)
