FREQUENCY_CLOCK = 3

class Text:
    def __init__(self, value):
        self.value = value

class Display:
    def __init__(self):
        self.frames = []

class Clock:
    def __init__(self):
        self.ticks = []

    def tick(self, framerate):
        self.ticks.append(framerate)

clock = Clock()

class Params:
    def __init__(self, width_rectangle, height_reference, arr, i, j):
        self.width_reference = width_rectangle
        self.height_reference = height_reference
        self.arr = arr
        self.i = i
        self.j = j

def draw_array(display, arrTexts, params):
    textos = tuple(text.value for text in arrTexts)
    display.frames.append((textos, tuple(params.i, params.j), params.width_reference, params.height_reference))

def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]

def compare_elements(display, arrTexts, params):
    draw_array(display, arrTexts, params)
    clock.tick(FREQUENCY_CLOCK)
    if (params.arr[params.i] > params.arr[params.j] and params.i < params.j) or (params.arr[params.i] < params.arr[params.j] and params.i > params.j):
        return False
    return True

def compare_and_swap(display, arrTexts, params):
    swapped = False
    draw_array(display, arrTexts, params)
    clock.tick(FREQUENCY_CLOCK)
    if (params.arr[params.i] > params.arr[params.j] and params.i < params.j) or (params.arr[params.i] < params.arr[params.j] and params.i > params.j):
        swap_elements(params.arr, arrTexts, params.i, params.j)
        draw_array(display, arrTexts, params)
        clock.tick(FREQUENCY_CLOCK)
        swapped = True
    draw_array(display, arrTexts, params)
    clock.tick(FREQUENCY_CLOCK)
    return swapped

def simulate_quicksort(arr, arrTexts, display, width_reference, height_reference):
    def partition(arr, arrTexts, display, width_reference, height_reference, low, high):
        i = low - 1
        for j in range(low, high):
            params = Params(width_reference, height_reference, arr, j, high)
            if compare_elements(display, arrTexts, params):
                i += 1
                if i != j:
                    compare_and_swap(display, arrTexts, Params(width_reference, height_reference, arr, i, j))
        if i + 1 != high:
            compare_and_swap(display, arrTexts, Params(width_reference, height_reference, arr, i + 1, high))
        return i + 1

    def quicksort(arr, arrTexts, display, width_reference, height_reference, low, high):
        if low < high:
            pi = partition(arr, arrTexts, display, width_reference, height_reference, low, high)
            quicksort(arr, arrTexts, display, width_reference, height_reference, low, pi - 1)
            quicksort(arr, arrTexts, display, width_reference, height_reference, pi + 1, high)

    quicksort(arr, arrTexts, display, width_reference, height_reference, 0, len(arr) - 1)
    draw_array(display, arrTexts, Params(width_reference, height_reference, arr, None, None))
    clock.tick(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    display = Display()
    clock.ticks.clear()
    simulate_quicksort(arr, textos, display, 40, 100)
    return arr, display.frames, list(clock.ticks)
