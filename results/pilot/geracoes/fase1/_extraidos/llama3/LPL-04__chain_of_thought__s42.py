class QuicksortParams:
    def __init__(self, arr, arrTexts, display, width_reference, height_reference):
        self.arr = arr
        self.arrTexts = arrTexts
        self.display = display
        self.width_reference = width_reference
        self.height_reference = height_reference

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

FREQUENCY_CLOCK = 3

def draw_array(display, arrTexts, width_rectangle, height_reference, poses_elevated=()):
    textos = tuple(texto.valor for texto in arrTexts)
    display.quadros.append((textos, tuple(poses_elevated), width_rectangle, height_reference))

def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]

def compare_elements(display, arrTexts, width_reference, height_reference, arr, i, j):
    textos = tuple(texto.valor for texto in arrTexts)
    display.quadros.append((textos, tuple([i, j]), width_reference, height_reference))
    clock.tick(FREQUENCY_CLOCK)
    textos = tuple(texto.valor for texto in arrTexts)
    display.quadros.append((textos, tuple([i, j]), width_reference, height_reference))
    clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        return False
    return True

def compare_and_swap(display, arrTexts, width_reference, height_reference, arr, i, j):
    textos = tuple(texto.valor for texto in arrTexts)
    display.quadros.append((textos, tuple([i, j]), width_reference, height_reference))
    clock.tick(FREQUENCY_CLOCK)
    textos = tuple(texto.valor for texto in arrTexts)
    display.quadros.append((textos, tuple([i, j]), width_reference, height_reference))
    clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        swap_elements(arr, arrTexts, i, j)
        textos = tuple(texto.valor for texto in arrTexts)
        display.quadros.append((textos, tuple([i, j]), width_reference, height_reference))
        clock.tick(FREQUENCY_CLOCK)
        return True
    return False

def simulate_quicksort(params):
    def partition(arr, arrTexts, display, width_reference, height_reference, low, high):
        i = low - 1
        for j in range(low, high):
            if compare_elements(
                display, arrTexts, width_reference, height_reference, arr, j, high
            ):
                i += 1
                if i != j:
                    compare_and_swap(
                        display, arrTexts, width_reference, height_reference, arr, i, j
                    )
        if i + 1 != high:
            compare_and_swap(
                display, arrTexts, width_reference, height_reference, arr, i + 1, high
            )
        return i + 1

    def quicksort(arr, arrTexts, display, width_reference, height_reference, low, high):
        if low < high:
            pi = partition(
                arr, arrTexts, display, width_reference, height_reference, low, high
            )
            quicksort(
                arr, arrTexts, display, width_reference, height_reference, low, pi - 1
            )
            quicksort(
                arr, arrTexts, display, width_reference, height_reference, pi + 1, high
            )

    quicksort(
        params.arr, params.arrTexts, params.display, params.width_reference, params.height_reference, 0, len(params.arr) - 1
    )
    draw_array(params.display, params.arrTexts, params.width_reference, params.height_reference)
    clock.tick(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = _Tela()
    clock.ticks.clear()
    params = QuicksortParams(arr, textos, tela, 40, 100)
    simulate_quicksort(params)
    return arr, tela.quadros, list(clock.ticks)
