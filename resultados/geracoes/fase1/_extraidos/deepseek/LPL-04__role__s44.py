FREQUENCY_CLOCK = 3

class Texto:
    def __init__(self, valor):
        self.valor = valor

class Tela:
    def __init__(self):
        self.quadros = []

class Relogio:
    def __init__(self):
        self.ticks = []

    def tick(self, framerate):
        self.ticks.append(framerate)

clock = Relogio()

class ParameterObject:
    def __init__(self, display, arrTexts, width_reference, height_reference, arr, i, j):
        self.display = display
        self.arrTexts = arrTexts
        self.width_reference = width_reference
        self.height_reference = height_reference
        self.arr = arr
        self.i = i
        self.j = j

def draw_array(parameterObject):
    textos = tuple(texto.valor for texto in parameterObject.arrTexts)
    parameterObject.display.quadros.append((textos, tuple(parameterObject.i, parameterObject.j), parameterObject.width_reference, parameterObject.height_reference))

def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]

def compare_elements(parameterObject):
    draw_array(parameterObject)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(parameterObject)
    clock.tick(FREQUENCY_CLOCK)
    if (parameterObject.arr[parameterObject.i] > parameterObject.arr[parameterObject.j] and parameterObject.i < parameterObject.j) or (parameterObject.arr[parameterObject.i] < parameterObject.arr[parameterObject.j] and parameterObject.i > parameterObject.j):
        return False
    return True

def compare_and_swap(parameterObject):
    swapped = False
    draw_array(parameterObject)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(parameterObject)
    clock.tick(FREQUENCY_CLOCK)
    if (parameterObject.arr[parameterObject.i] > parameterObject.arr[parameterObject.j] and parameterObject.i < parameterObject.j) or (parameterObject.arr[parameterObject.i] < parameterObject.arr[parameterObject.j] and parameterObject.i > parameterObject.j):
        swap_elements(parameterObject.arr, parameterObject.arrTexts, parameterObject.i, parameterObject.j)
        draw_array(parameterObject)
        clock.tick(FREQUENCY_CLOCK)
        swapped = True
    draw_array(parameterObject)
    clock.tick(FREQUENCY_CLOCK)
    return swapped

def simulate_quicksort(arr, arrTexts, display, width_reference, height_reference):
    def partition(parameterObject):
        i = parameterObject.low - 1
        for j in range(parameterObject.low, parameterObject.high):
            if compare_elements(parameterObject):
                i += 1
                if i != j:
                    compare_and_swap(parameterObject)
        if i + 1 != parameterObject.high:
            compare_and_swap(parameterObject)
        return i + 1

    def quicksort(parameterObject):
        if parameterObject.low < parameterObject.high:
            pi = partition(parameterObject)
            quicksort(parameterObject)
            quicksort(parameterObject)

    parameterObject = ParameterObject(display, arrTexts, width_reference, height_reference, arr, 0, len(arr) - 1)
    quicksort(parameterObject)
    draw_array(parameterObject)
    clock.tick(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = [Texto(str(x)) for x in arr]
    tela = Tela()
    clock.ticks.clear()
    simulate_quicksort(arr, textos, tela, 40, 100)
    return arr, tela.quadros, list(clock.ticks)
