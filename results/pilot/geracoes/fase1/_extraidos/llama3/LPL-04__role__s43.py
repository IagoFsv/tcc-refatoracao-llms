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


class AnimationParameters:
    def __init__(self, width_reference, height_reference):
        self.width_reference = width_reference
        self.height_reference = height_reference


def draw_array(display, arrTexts, params):
    textos = tuple(texto.valor for texto in arrTexts)
    display.quadros.append((textos, tuple(), params.width_reference, params.height_reference))


def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]


def compare_elements(display, arrTexts, params, i, j):
    draw_array(display, arrTexts, params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, params, [i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        return False
    return True


def compare_and_swap(display, arrTexts, params, i, j):
    swapped = False
    draw_array(display, arrTexts, params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, params, [i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        swap_elements(arr, arrTexts, i, j)
        draw_array(display, arrTexts, params, [i, j])
        clock.tick(FREQUENCY_CLOCK)
        swapped = True
    draw_array(display, arrTexts, params)
    clock.tick(FREQUENCY_CLOCK)
    return swapped


def simulate_quicksort(arr, arrTexts, display, params):
    def partition(arr, arrTexts, display, params, low, high):
        i = low - 1
        for j in range(low, high):
            if compare_elements(display, arrTexts, params, arr, j, high):
                i += 1
                if i != j:
                    compare_and_swap(display, arrTexts, params, i, j)
        if i + 1 != high:
            compare_and_swap(display, arrTexts, params, i + 1, high)
        return i + 1

    def quicksort(arr, arrTexts, display, params, low, high):
        if low < high:
            pi = partition(arr, arrTexts, display, params, low, high)
            quicksort(arr, arrTexts, display, params, low, pi - 1)
            quicksort(arr, arrTexts, display, params, pi + 1, high)

    quicksort(arr, arrTexts, display, params, 0, len(arr) - 1)
    draw_array(display, arrTexts, params)
    clock.tick(FREQUENCY_CLOCK)


def executar(valores):
    """Ordena uma copia de valores, animando cada passo. Ponto de entrada publico.

    Devolve (lista ordenada, quadros desenhados, taxas dos ticks do relogio).
    Cada quadro e (textos, posicoes destacadas, largura, altura).
    """
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = _Tela()
    clock.ticks.clear()
    simulate_quicksort(arr, textos, tela, AnimationParameters(40, 100))
    return arr, tela.quadros, list(clock.ticks)
