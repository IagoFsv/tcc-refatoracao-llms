from dataclasses import dataclass, asdict

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


def draw_array(display: Tela, arrTexts: list[Texto], width_rectangle: int, height_reference: int, poses_elevated: tuple = ()):
    textos = tuple(texto.valor for texto in arrTexts)
    display.quadros.append((textos, tuple(poses_elevated), width_rectangle, height_reference))


def swap_elements(arr: list, arrText: list[Texto], i: int, j: int):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]


def compare_elements(display: Tela, arrTexts: list[Texto], width_reference: int, height_reference: int, arr: list, i: int, j: int) -> bool:
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(3)
    draw_array(display, arrTexts, width_reference, height_reference, [i, j])
    clock.tick(3)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        return False
    return True


def compare_and_swap(display: Tela, arrTexts: list[Texto], width_reference: int, height_reference: int, arr: list, i: int, j: int) -> bool:
    swapped = False
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(3)
    draw_array(display, arrTexts, width_reference, height_reference, [i, j])
    clock.tick(3)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        swap_elements(arr, arrTexts, i, j)
        draw_array(display, arrTexts, width_reference, height_reference, [i, j])
        clock.tick(3)
        swapped = True
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(3)
    return swapped


def simulate_quicksort(arr: list, arrTexts: list[Texto], display: Tela, width_reference: int, height_reference: int):
    def partition(arr: list, arrTexts: list[Texto], display: Tela, width_reference: int, height_reference: int, low: int, high: int) -> int:
        i = low - 1
        for j in range(low, high):
            if compare_elements(display, arrTexts, width_reference, height_reference, arr, j, high):
                i += 1
                if i != j:
                    compare_and_swap(display, arrTexts, width_reference, height_reference, arr, i, j)
        if i + 1 != high:
            compare_and_swap(display, arrTexts, width_reference, height_reference, arr, i + 1, high)
        return i + 1

    def quicksort(arr: list, arrTexts: list[Texto], display: Tela, width_reference: int, height_reference: int, low: int, high: int):
        if low < high:
            pi = partition(arr, arrTexts, display, width_reference, height_reference, low, high)
            quicksort(arr, arrTexts, display, width_reference, height_reference, low, pi - 1)
            quicksort(arr, arrTexts, display, width_reference, height_reference, pi + 1, high)

    quicksort(arr, arrTexts, display, width_reference, height_reference, 0, len(arr) - 1)
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(3)


def executar(valores: list) -> tuple[list, list, list]:
    arr = list(valores)
    textos = [Texto(str(x)) for x in arr]
    tela = Tela()
    clock.ticks.clear()
    simulate_quicksort(arr, textos, tela, 40, 100)
    return arr, tela.quadros, list(clock.ticks)
