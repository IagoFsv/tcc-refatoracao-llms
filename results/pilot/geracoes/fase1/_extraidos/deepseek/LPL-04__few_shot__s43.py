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

class Parametros:
    def __init__(self, width_reference, height_reference, arr, i, j):
        self.width_reference = width_reference
        self.height_reference = height_reference
        self.arr = arr
        self.i = i
        self.j = j

clock = Relogio([])

def draw_array(display, arrTexts, parametros:Parametros):
    textos = tuple(texto.valor for texto in arrTexts)
    display.quadros.append((textos, (parametros.i, parametros.j), parametros.width_reference, parametros.height_reference))

def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]

def compare_elements(display, arrTexts, parametros:Parametros):
    draw_array(display, arrTexts, parametros)
    clock.ticks.append(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, parametros)
    if (parametros.arr[parametros.i] > parametros.arr[parametros.j] and parametros.i < parametros.j) or (parametros.arr[parametros.i] < parametros.arr[parametros.j] and parametros.i > parametros.j):
        return False
    return True

def compare_and_swap(display, arrTexts, parametros:Parametros):
    swapped = False
    draw_array(display, arrTexts, parametros)
    clock.ticks.append(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, parametros)
    if (parametros.arr[parametros.i] > parametros.arr[parametros.j] and parametros.i < parametros.j) or (parametros.arr[parametros.i] < parametros.arr[parametros.j] and parametros.i > parametros.j):
        swap_elements(parametros.arr, arrTexts, parametros.i, parametros.j)
        draw_array(display, arrTexts, parametros)
        clock.ticks.append(FREQUENCY_CLOCK)
        swapped = True
    draw_array(display, arrTexts, parametros)
    clock.ticks.append(FREQUENCY_CLOCK)
    return swapped

def simulate_quicksort(arr, arrTexts, display, width_reference, height_reference):
    def partition(arr, arrTexts, display, width_reference, height_reference, low, high):
        i = low - 1
        for j in range(low, high):
            parametros = Parametros(width_reference, height_reference, arr, j, high)
            if compare_elements(display, arrTexts, parametros):
                i += 1
                if i != j:
                    parametros = Parametros(width_reference, height_reference, arr, i, j)
                    compare_and_swap(display, arrTexts, parametros)
        if i + 1 != high:
            parametros = Parametros(width_reference, height_reference, arr, i + 1, high)
            compare_and_swap(display, arrTexts, parametros)
        return i + 1

    def quicksort(arr, arrTexts, display, width_reference, height_reference, low, high):
        if low < high:
            pi = partition(arr, arrTexts, display, width_reference, height_reference, low, high)
            quicksort(arr, arrTexts, display, width_reference, height_reference, low, pi - 1)
            quicksort(arr, arrTexts, display, width_reference, height_reference, pi + 1, high)

    quicksort(arr, arrTexts, display, width_reference, height_reference, 0, len(arr) - 1)
    draw_array(display, arrTexts, Parametros(width_reference, height_reference, arr, None, None))
    clock.ticks.append(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = Tela([])
    clock.ticks.clear()
    simulate_quicksort(arr, textos, tela, 40, 100)
    return arr, tela.quadros, list(clock.ticks)
