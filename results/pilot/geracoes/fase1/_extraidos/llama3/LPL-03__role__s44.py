class AnimationParams:
    def __init__(self, values, texts, width, height):
        self.values = values
        self.texts = texts
        self.width = width
        self.height = height


def executar(params):
    values = list(params.values)
    texts = [_Texto(str(x)) for x in values]
    tela = _Tela()
    clock = _Relogio()
    clock.ticks.clear()
    simulate_heapsort(values, texts, tela, params.width, params.height)
    return values, tela.quadros, list(clock.ticks)


def simulate_heapsort(arr, arrTexts, display, params):
    def heapify(arr, arrTexts, display, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and compare_elements(
            display, arrTexts, params.width, params.height, arr, largest, l
        ):
            largest = l
        if r < n and compare_elements(
            display, arrTexts, params.width, params.height, arr, largest, r
        ):
            largest = r
        if largest != i:
            compare_elements(
                display, arrTexts, params.width, params.height, arr, i, largest
            )
            swap_elements(arr, arrTexts, i, largest)
            heapify(arr, arrTexts, display, n, largest)

    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, arrTexts, display, n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(arr, arrTexts, i, 0)
        heapify(arr, arrTexts, display, i, 0)
    draw_array(display, arrTexts, params.width, params.height)
    clock.tick(FREQUENCY_CLOCK)
    return arr, tela.quadros, list(clock.ticks)
