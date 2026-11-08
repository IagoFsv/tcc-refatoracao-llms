class Display:
    def __init__(self):
        self.quadros = []

    def quadro(self, textos, posicoes_elevadas, largura, altura):
        self.quadros.append((textos, posicoes_elevadas, largura, altura))


class Relogio:
    def __init__(self):
        self.ticks = []

    def tick(self, framerate):
        self.ticks.append(framerate)


FREQUENCY_CLOCK = 3


class Elemento:
    def __init__(self, valor):
        self.valor = valor


class Quadro:
    def __init__(self, textos, posicoes_elevadas, largura, altura):
        self.textos = textos
        self.posicoes_elevadas = posicoes_elevadas
        self.largura = largura
        self.altura = altura


class Estado:
    def __init__(self, arr, arrTexts, display, width_reference, height_reference):
        self.arr = arr
        self.arrTexts = arrTexts
        self.display = display
        self.width_reference = width_reference
        self.height_reference = height_reference


def draw_array(display, arrTexts, width_rectangle, height_reference, poses_elevated=()):
    textos = tuple(texto.valor for texto in arrTexts)
    display.quadro(textos, tuple(poses_elevated), width_rectangle, height_reference)


def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]


def compare_elements(display, arrTexts, *args):
    width_reference, height_reference, arr, i, j = args
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(display, arrTexts, width_reference, height_reference, [i, j])
    clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        return False
    return True


def heapify(display, arrTexts, arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and compare_elements(
        display, arrTexts, arr, largest, l
    ):
        largest = l
    if r < n and compare_elements(
        display, arrTexts, arr, largest, r
    ):
        largest = r
    if largest != i:
        compare_elements(
            display, arrTexts, arr, i, largest
        )
        swap_elements(arr, arrTexts, i, largest)
        heapify(display, arrTexts, arr, n, largest)


def simulate_heapsort(arr, arrTexts, display, width_reference, height_reference):
    n = len(arr)
    for i in range(n, -1, -1):
        heapify(display, arrTexts, arr, n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(arr, arrTexts, i, 0)
        heapify(display, arrTexts, arr, i, 0)
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)


def executar(valores):
    arr = list(valores)
    textos = [Elemento(str(x)) for x in arr]
    tela = Display()
    clock = Relogio()
    clock.ticks.clear()
    estado = Estado(arr, textos, tela, 40, 100)
    simulate_heapsort(estado.arr, estado.arrTexts, estado.display, estado.width_reference, estado.height_reference)
    return estado.arr, estado.display.quadros, list(clock.ticks)
