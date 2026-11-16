from dataclasses import dataclass, asdict

@dataclass
class Quadro:
    textos: tuple
    poses_elevated: tuple
    width_rectangle: int
    height_reference: int

@dataclass
class Relogio:
    ticks: list

def draw_array(display: _Tela, quadro: Quadro):
    display.quadros.append(quadro)

def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]

def compare_elements(display: _Tela, arrTexts, *args):
    width_reference, height_reference, arr, i, j = args
    draw_array(display, Quadro(textos=tuple(texto.valor for texto in arrTexts), poses_elevated=(i, j), width_rectangle=width_reference, height_reference=height_reference))
    display.clock.tick(FREQUENCY_CLOCK)
    draw_array(display, Quadro(textos=tuple(texto.valor for texto in arrTexts), poses_elevated=(i, j), width_rectangle=width_reference, height_reference=height_reference))
    display.clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        return False
    return True

def compare_and_swap(display: _Tela, arrTexts, *args):
    width_reference, height_reference, arr, i, j = args
    swapped = False
    draw_array(display, Quadro(textos=tuple(texto.valor for texto in arrTexts), poses_elevated=(i, j), width_rectangle=width_reference, height_reference=height_reference))
    display.clock.tick(FREQUENCY_CLOCK)
    draw_array(display, Quadro(textos=tuple(texto.valor for texto in arrTexts), poses_elevated=(i, j), width_rectangle=width_reference, height_reference=height_reference))
    display.clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        swap_elements(arr, arrTexts, i, j)
        draw_array(display, Quadro(textos=tuple(texto.valor for texto in arrTexts), poses_elevated=(i, j), width_rectangle=width_reference, height_reference=height_reference))
        display.clock.tick(FREQUENCY_CLOCK)
        swapped = True
    draw_array(display, Quadro(textos=tuple(texto.valor for texto in arrTexts), poses_elevated=(), width_rectangle=width_reference, height_reference=height_reference))
    display.clock.tick(FREQUENCY_CLOCK)
    return swapped

def simulate_quicksort(arr, arrTexts, display: _Tela, width_reference, height_reference):
    def partition(arr, arrTexts, display, width_reference, height_reference, low, high):
        i = low - 1
        for j in range(low, high):
            if compare_elements(display, arrTexts, width_reference, height_reference, arr, j, high):
                i += 1
                if i != j:
                    compare_and_swap(display, arrTexts, width_reference, height_reference, arr, i, j)
        if i + 1 != high:
            compare_and_swap(display, arrTexts, width_reference, height_reference, arr, i + 1, high)
        return i + 1

    def quicksort(arr, arrTexts, display, width_reference, height_reference, low, high):
        if low < high:
            pi = partition(arr, arrTexts, display, width_reference, height_reference, low, high)
            quicksort(arr, arrTexts, display, width_reference, height_reference, low, pi - 1)
            quicksort(arr, arrTexts, display, width_reference, height_reference, pi + 1, high)

    quicksort(arr, arrTexts, display, width_reference, height_reference, 0, len(arr) - 1)
    draw_array(display, Quadro(textos=tuple(texto.valor for texto in arrTexts), poses_elevated=(), width_rectangle=width_reference, height_reference=height_reference))
    display.clock.tick(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = _Tela()
    clock = Relogio()
    clock.ticks.clear()
    simulate_quicksort(arr, textos, tela, 40, 100)
    return arr, tela.quadros, list(clock.ticks)
