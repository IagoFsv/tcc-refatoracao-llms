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


class DisplayParams:
    def __init__(self, width_rectangle, height_reference, poses_elevated=()):
        self.width_rectangle = width_rectangle
        self.height_reference = height_reference
        self.poses_elevated = poses_elevated


class AnimationParams:
    def __init__(self, arr, arrText, display, width_rectangle, height_reference):
        self.arr = arr
        self.arrText = arrText
        self.display = display
        self.width_rectangle = width_rectangle
        self.height_reference = height_reference


clock = _Relogio()


def draw_array(params: AnimationParams, display_params: DisplayParams):
    textos = tuple(texto.valor for texto in params.arrText)
    params.display.quadros.append((textos, tuple(display_params.poses_elevated), display_params.width_rectangle, display_params.height_reference))


def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]


def compare_elements(display_params: DisplayParams, animation_params: AnimationParams, i, j):
    draw_array(animation_params, display_params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(animation_params, display_params, DisplayParams(animation_params.width_rectangle, animation_params.height_reference, [i, j]))
    clock.tick(FREQUENCY_CLOCK)
    if (animation_params.arr[i] > animation_params.arr[j] and i < j) or (animation_params.arr[i] < animation_params.arr[j] and i > j):
        return False
    return True


def simulate_heapsort(animation_params: AnimationParams, display_params: DisplayParams):
    def heapify(animation_params: AnimationParams, display_params: DisplayParams, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and compare_elements(display_params, animation_params, largest, l):
            largest = l
        if r < n and compare_elements(display_params, animation_params, largest, r):
            largest = r
        if largest != i:
            compare_elements(display_params, animation_params, i, largest)
            swap_elements(animation_params.arr, animation_params.arrText, i, largest)
            heapify(animation_params, display_params, n, largest)

    n = len(animation_params.arr)
    for i in range(n, -1, -1):
        heapify(animation_params, display_params, n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(animation_params.arr, animation_params.arrText, i, 0)
        heapify(animation_params, display_params, i, 0)
    draw_array(animation_params, display_params)


def executar(valores):
    """Ordena uma copia de valores, animando cada passo. Ponto de entrada publico.

    Devolve (lista ordenada, quadros desenhados, taxas dos ticks do relogio).
    Cada quadro e (textos, posicoes destacadas, largura, altura).
    """
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = _Tela()
    clock.ticks.clear()
    simulate_heapsort(AnimationParams(arr, textos, tela, 40, 100), DisplayParams(40, 100))
    return arr, tela.quadros, list(clock.ticks)
