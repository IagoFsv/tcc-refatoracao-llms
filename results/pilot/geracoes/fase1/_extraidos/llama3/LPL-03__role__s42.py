from dataclasses import dataclass

FREQUENCY_CLOCK = 3


@dataclass
class Texto:
    valor: str


@dataclass
class Tela:
    quadros: list


@dataclass
class Relogio:
    ticks: list


clock = Relogio()


def draw_array(display, arrTexts, width_rectangle, height_reference, poses_elevated=()):
    textos = tuple(texto.valor for texto in arrTexts)
    display.quadros.append((textos, tuple(poses_elevated), width_rectangle, height_reference))


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


def simulate_heapsort(arr, arrTexts, display, width_reference, height_reference):
    heapify(arr, arrTexts, display, width_reference, height_reference)
    for i in range(len(arr) - 1, 0, -1):
        swap_elements(arr, arrTexts, i, 0)
        heapify(arr, arrTexts, display, width_reference, height_reference)
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)


def heapify(arr, arrTexts, display, width_reference, height_reference, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and compare_elements(
        display, arrTexts, width_reference, height_reference, arr, largest, l
    ):
        largest = l
    if r < n and compare_elements(
        display, arrTexts, width_reference, height_reference, arr, largest, r
    ):
        largest = r
    if largest != i:
        compare_elements(
            display, arrTexts, width_reference, height_reference, arr, i, largest
        )
        swap_elements(arr, arrTexts, i, largest)
        heapify(
            arr, arrTexts, display, width_reference, height_reference, n, largest
        )


def executar(valores):
    arr = list(valores)
    textos = [Texto(str(x)) for x in arr]
    tela = Tela()
    clock.ticks.clear()
    simulate_heapsort(arr, textos, tela, 40, 100)
    return arr, tela.quadros, list(clock.ticks)
