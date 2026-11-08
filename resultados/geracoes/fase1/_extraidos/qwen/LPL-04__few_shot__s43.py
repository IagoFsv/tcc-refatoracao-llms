class Display:
    def __init__(self):
        self.quadros = []

    def quadro(self, textos, posicoes_elevated, width_rectangle, height_reference):
        self.quadros.append((textos, tuple(posicoes_elevated), width_rectangle, height_reference))


class Relogio:
    def __init__(self):
        self.ticks = []

    def tick(self, framerate):
        self.ticks.append(framerate)


class ParametrosOrdenacao:
    def __init__(self, display, arrTexts, width_reference, height_reference, posicoes_elevated=()):
        self.display = display
        self.arrTexts = arrTexts
        self.width_reference = width_reference
        self.height_reference = height_reference
        self.posicoes_elevated = posicoes_elevated


clock = Relogio()
display = Display()


def draw_array(params):
    textos = tuple(texto.valor for texto in params.arrTexts)
    params.display.quadro(textos, params.posicoes_elevated, params.width_reference, params.height_reference)


def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]


def compare_elements(params, *args):
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(params, *args)
    clock.tick(FREQUENCY_CLOCK)
    if (args[3][i] > args[3][j] and i < j) or (args[3][i] < args[3][j] and i > j):
        return False
    return True


def compare_and_swap(params, *args):
    swapped = False
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(params, *args)
    clock.tick(FREQUENCY_CLOCK)
    if (args[3][i] > args[3][j] and i < j) or (args[3][i] < args[3][j] and i > j):
        swap_elements(args[3], args[4], i, j)
        draw_array(params, *args)
        clock.tick(FREQUENCY_CLOCK)
        swapped = True
    draw_array(params)
    clock.tick(FREQUENCY_CLOCK)
    return swapped


def partition(arr, arrTexts, params, low, high):
    i = low - 1
    for j in range(low, high):
        if compare_elements(params, arrTexts, params.width_reference, params.height_reference, arr, j, high):
            i += 1
            if i != j:
                compare_and_swap(params, arrTexts, params.width_reference, params.height_reference, arr, i, j)
    if i + 1 != high:
        compare_and_swap(params, arrTexts, params.width_reference, params.height_reference, arr, i + 1, high)
    return i + 1


def quicksort(arr, arrTexts, params, low, high):
    if low < high:
        pi = partition(arr, arrTexts, params, low, high)
        quicksort(arr, arrTexts, params, low, pi - 1)
        quicksort(arr, arrTexts, params, pi + 1, high)


def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = Display()
    clock.ticks.clear()
    params = ParametrosOrdenacao(tela, textos, 40, 100)
    quicksort(arr, textos, params, 0, len(arr) - 1)
    return arr, tela.quadros, list(clock.ticks)
