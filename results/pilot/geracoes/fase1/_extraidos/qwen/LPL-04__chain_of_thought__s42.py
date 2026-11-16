class Parameters:
    def __init__(self, display, arrTexts, width_rectangle, height_reference, poses_elevated=()):
        self.display = display
        self.arrTexts = arrTexts
        self.width_rectangle = width_rectangle
        self.height_reference = height_reference
        self.poses_elevated = poses_elevated


FREQUENCY_CLOCK = 3


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


clock = _Relogio()


def draw_array(params: Parameters):
    textos = tuple(texto.valor for texto in params.arrTexts)
    params.display.quadros.append((textos, tuple(params.poses_elevated), params.width_rectangle, params.height_reference))


def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]


def compare_elements(params: Parameters, i, j):
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(params, poses_elevated=[i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (params.arr[i] > params.arr[j] and i < j) or (params.arr[i] < params.arr[j] and i > j):
        return False
    return True


def compare_and_swap(params: Parameters, i, j):
    swapped = False
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(params, poses_elevated=[i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (params.arr[i] > params.arr[j] and i < j) or (params.arr[i] < params.arr[j] and i > j):
        swap_elements(params.arr, params.arrText, i, j)
        draw_array(params, poses_elevated=[i, j])
        clock.tick(FREQUENCY_CLOCK)
        swapped = True
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)
    return swapped


def partition(params: Parameters, low, high):
    i = low - 1
    for j in range(low, high):
        if compare_elements(params, j, high):
            i += 1
            if i != j:
                compare_and_swap(params, i, j)
    if i + 1 != high:
        compare_and_swap(params, i + 1, high)
    return i + 1


def quicksort(params: Parameters, low, high):
    if low < high:
        pi = partition(params, low, high)
        quicksort(params, low, pi - 1)
        quicksort(params, pi + 1, high)


def simulate_quicksort(arr, arrTexts, display, width_reference, height_reference):
    params = Parameters(display, arrTexts, width_reference, height_reference)
    params.arr = list(arr)
    params.arrText = [_Texto(str(x)) for x in arr]
    params.display = _Tela()
    clock.ticks.clear()
    quicksort(params, 0, len(arr) - 1)
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)


def executar(valores):
    display = _Tela()
    arrTexts = [_Texto(str(x)) for x in valores]
    tela = _Tela()
    clock.ticks.clear()
    simulate_quicksort(valores, arrTexts, display, 40, 100)
    return list(valores), tela.quadros, list(clock.ticks)
