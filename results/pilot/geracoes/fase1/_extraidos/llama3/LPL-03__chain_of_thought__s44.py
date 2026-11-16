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


def draw_array(display, arrTexts, width_rectangle, height_reference, poses_elevated=()):
    textos = tuple(texto.valor for texto in arrTexts)
    display.quadros.append((textos, tuple(poses_elevated), width_rectangle, height_reference))


def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]


def compare_elements(options):
    width_reference, height_reference = options.width_reference, options.height_reference
    draw_array(options.display, options.arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(options.display, options.arrTexts, width_reference, height_reference, [options.i, options.j])
    clock.tick(FREQUENCY_CLOCK)
    if (options.arr[options.i] > options.arr[options.j] and options.i < options.j) or (options.arr[options.i] < options.arr[options.j] and options.i > options.j):
        return False
    return True


def heapify(options):
    largest = options.i
    l = 2 * options.i + 1
    r = 2 * options.i + 2
    if l < options.n and compare_elements(options):
        largest = l
    if r < options.n and compare_elements(options):
        largest = r
    if largest != options.i:
        compare_elements(options)
        swap_elements(options.arr, options.arrTexts, options.i, largest)
        heapify(HeapifyOptions(options.arr, options.arrTexts, options.display, options.width_reference, options.height_reference, options.n, largest))


def simulate_heapsort(arr, arrTexts, display, width_reference, height_reference):
    n = len(arr)
    for i in range(n, -1, -1):
        heapify(HeapifyOptions(arr, arrTexts, display, width_reference, height_reference, n, i))
    for i in range(n - 1, 0, -1):
        swap_elements(arr, arrTexts, i, 0)
        heapify(HeapifyOptions(arr, arrTexts, display, width_reference, height_reference, i, 0))
    draw_array(display, arrTexts, width_reference, height_reference)
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
