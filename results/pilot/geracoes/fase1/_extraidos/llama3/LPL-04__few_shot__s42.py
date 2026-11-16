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

class Tela:
    def __init__(self):
        self.quadros = []

    def append(self, quadro: Quadro):
        self.quadros.append(quadro)

class Relogio:
    def __init__(self):
        self.ticks = []

    def tick(self, framerate):
        self.ticks.append(framerate)

def draw_array(display: Tela, arrTexts: tuple, width_rectangle: int, height_reference: int, poses_elevated=()):
    display.append(Quadro(arrTexts, poses_elevated, width_rectangle, height_reference))

def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]

def compare_elements(display: Tela, arrTexts: tuple, width_reference: int, height_reference: int, i: int, j: int) -> bool:
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, width_reference, height_reference, [i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        return False
    return True

def compare_and_swap(display: Tela, arrTexts: tuple, width_reference: int, height_reference: int, i: int, j: int) -> bool:
    swapped = False
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, width_reference, height_reference, [i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        swap_elements(arr, arrTexts, i, j)
        draw_array(display, arrTexts, width_reference, height_reference, [i, j])
        clock.tick(FREQUENCY_CLOCK)
        swapped = True
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)
    return swapped

def simulate_quicksort(arr, arrTexts, display: Tela, width_reference: int, height_reference: int):
    def partition(arr, arrTexts, display, width_reference, height_reference, low, high):
        i = low - 1
        for j in range(low, high):
            if compare_elements(display, arrTexts, width_reference, height_reference, arr, j, high):
                i += 1
                if i != j:
                    compare_and_swap(display, arrTexts, width_reference, height_reference, arr, i, j)
        if i + 1 != high:
            compare_and_swap(display, arrTexts, width_reference, height_reference, arr, i + 1, high)
        return i + 1

    def quicksort(arr, arrTexts, display, width_reference, height_reference, low, high):
        if low < high:
            pi = partition(arr, arrTexts, display, width_reference, height_reference, low, high)
            quicksort(arr, arrTexts, display, width_reference, height_reference, low, pi - 1)
            quicksort(arr, arrTexts, display, width_reference, height_reference, pi + 1, high)

    quicksort(arr, arrTexts, display, width_reference, height_reference, 0, len(arr) - 1)
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = tuple(Texto(str(x)) for x in arr)
    tela = Tela()
    clock.ticks.clear()
    simulate_quicksort(arr, textos, tela, 40, 100)
    return arr, tela.quadros, list(clock.ticks)
