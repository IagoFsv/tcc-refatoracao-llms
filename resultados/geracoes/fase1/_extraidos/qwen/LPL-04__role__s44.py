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


class AnimationParams:
    def __init__(self, display, arrTexts, width_rectangle, height_reference, poses_elevated=()):
        self.display = display
        self.arrTexts = arrTexts
        self.width_rectangle = width_rectangle
        self.height_reference = height_reference
        self.poses_elevated = poses_elevated


clock = _Relogio()


def draw_array(params):
    textos = tuple(texto.valor for texto in params.arrTexts)
    params.display.quadros.append((textos, tuple(params.poses_elevated), params.width_rectangle, params.height_reference))


def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]


def compare_elements(params, *args):
    arr, i, j = args
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(AnimationParams(params.display, params.arrTexts, params.width_rectangle, params.height_reference, [i, j]))
    clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        return False
    return True


def compare_and_swap(params, *args):
    arr, i, j = args
    swapped = False
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(AnimationParams(params.display, params.arrTexts, params.width_rectangle, params.height_reference, [i, j]))
    clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        swap_elements(arr, params.arrTexts, i, j)
        draw_array(AnimationParams(params.display, params.arrTexts, params.width_rectangle, params.height_reference, [i, j]))
        clock.tick(FREQUENCY_CLOCK)
        swapped = True
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)
    return swapped


def simulate_quicksort(arr, arrTexts, display, width_reference, height_reference):
    def partition(arr, arrTexts, display, width_reference, height_reference, low, high):
        i = low - 1
        for j in range(low, high):
            if compare_elements(
                AnimationParams(display, arrTexts, width_reference, height_reference), arr, j, high
            ):
                i += 1
                if i != j:
                    compare_and_swap(
                        AnimationParams(display, arrTexts, width_reference, height_reference), arr, i, j
                    )
        if i + 1 != high:
            compare_and_swap(
                AnimationParams(display, arrTexts, width_reference, height_reference), arr, i + 1, high
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
        arr, arrTexts, display, width_reference, height_reference, 0, len(arr) - 1
    )
    draw_array(AnimationParams(display, arrTexts, width_reference, height_reference))
    clock.tick(FREQUENCY_CLOCK)


def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = _Tela()
    clock.ticks.clear()
    simulate_quicksort(arr, textos, tela, 40, 100)
    return arr, tela.quadros, list(clock.ticks)
