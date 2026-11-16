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


class _ParametrosAnimacao:
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


def compare_elements(params, i, j):
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(params, poses_elevated=[i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (params.arr[i] > params.arr[j] and i < j) or (params.arr[i] < params.arr[j] and i > j):
        return False
    return True


def heapify(params, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and compare_elements(params, largest, l):
        largest = l
    if r < n and compare_elements(params, largest, r):
        largest = r
    if largest != i:
        compare_elements(params, i, largest)
        swap_elements(params.arr, params.arrText, i, largest)
        heapify(params, n, largest)


def simulate_heapsort(arr, arrTexts, display, width_reference, height_reference):
    params = _ParametrosAnimacao(display, arrTexts, width_reference, height_reference)
    n = len(arr)
    for i in range(n, -1, -1):
        heapify(params, n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(arr, arrTexts, i, 0)
        heapify(params, i, 0)
    draw_array(params)
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
    simulate_heapsort(arr, textos, tela, 40, 100)
    return arr, tela.quadros, list(clock.ticks)
