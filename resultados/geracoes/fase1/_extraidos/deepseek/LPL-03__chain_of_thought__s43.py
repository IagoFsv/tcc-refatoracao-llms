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

class FrameParams:
    def __init__(self, display, arrTexts, width_rectangle, height_reference, poses_elevated=()):
        self.display = display
        self.arrTexts = arrTexts
        self.width_rectangle = width_rectangle
        self.height_reference = height_reference
        self.poses_elevated = poses_elevated

clock = Relogio()

def draw_array(frame_params):
    textos = tuple(texto.valor for texto in frame_params.arrTexts)
    frame_params.display.quadros.append((textos, tuple(frame_params.poses_elevated), frame_params.width_rectangle, frame_params.height_reference))

def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]

def compare_elements(frame_params, arr, i, j):
    draw_array(frame_params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(frame_params)
    clock.tick(FREQUENCY_CLOCK)
    if (arr[i] > arr[j] and i < j) or (arr[i] < arr[j] and i > j):
        return False
    return True

def simulate_heapsort(arr, arrTexts, display, width_reference, height_reference):
    def heapify(arr, arrTexts, display, width_reference, height_reference, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and compare_elements(
            FrameParams(display, arrTexts, width_reference, height_reference), arr, largest, l
        ):
            largest = l
        if r < n and compare_elements(
            FrameParams(display, arrTexts, width_reference, height_reference), arr, largest, r
        ):
            largest = r
        if largest != i:
            compare_elements(
                FrameParams(display, arrTexts, width_reference, height_reference), arr, i, largest
            )
            swap_elements(arr, arrTexts, i, largest)
            heapify(
                arr, arrTexts, display, width_reference, height_reference, n, largest
            )

    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, arrTexts, display, width_reference, height_reference, n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(arr, arrTexts, i, 0)
        heapify(arr, arrTexts, display, width_reference, height_reference, i, 0)
    draw_array(FrameParams(display, arrTexts, width_reference, height_reference))
    clock.tick(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = Tela()
    clock.ticks.clear()
    simulate_heapsort(arr, textos, tela, 40, 100)
    return arr, tela.quadros, list(clock.ticks)
