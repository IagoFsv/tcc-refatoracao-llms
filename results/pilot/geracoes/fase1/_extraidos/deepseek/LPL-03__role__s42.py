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
    draw_array(display, arrTexts, params)
    clock.tick(FREQUENCY_CLOCK)
    if (params.arr[params.i] > params.arr[params.j] and params.i < params.j) or (params.arr[params.i] < params.arr[params.j] and params.i > params.j):
        return False
    return True

def simulate_heapsort(arr, arrTexts, display, width_reference, height_reference):
    def heapify(arr, arrTexts, display, params, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and compare_elements(display, arrTexts, Params(params.width_reference, params.height_reference, params.arr, largest, l)):
            largest = l
        if r < n and compare_elements(display, arrTexts, Params(params.width_reference, params.height_reference, params.arr, largest, r)):
            largest = r
        if largest != i:
            compare_elements(display, arrTexts, Params(params.width_reference, params.height_reference, params.arr, i, largest))
            swap_elements(arr, arrTexts, i, largest)
            heapify(arr, arrTexts, display, params, n, largest)

    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, arrTexts, display, Params(width_reference, height_reference, arr, n, i), n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(arr, arrTexts, i, 0)
        heapify(arr, arrTexts, display, Params(width_reference, height_reference, arr, i, 0), i, 0)
    draw_array(display, arrTexts, Params(width_reference, height_reference, arr, None, None))
    clock.tick(FREQUENCY_CLOCK)

def execute(values):
    arr = list(values)
    texts = [_Text(str(x)) for x in arr]
    display = Display()
    clock.ticks.clear()
    simulate_heapsort(arr, texts, display, 40, 100)
    return arr, display.frames, list(clock.ticks)
