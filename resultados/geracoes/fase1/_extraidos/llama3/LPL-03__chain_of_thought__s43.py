class HeapSortOptions:
    def __init__(self, arr, arrTexts, display, width_reference, height_reference):
        self.arr = arr
        self.arrTexts = arrTexts
        self.display = display
        self.width_reference = width_reference
        self.height_reference = height_reference

def simulate_heapsort(options):
    heapify(options.arr, options.arrTexts, options.display, options.width_reference, options.height_reference, len(options.arr), 0)
    for i in range(len(options.arr) - 1, 0, -1):
        swap_elements(options.arr, options.arrTexts, i, 0)
        heapify(options.arr, options.arrTexts, options.display, options.width_reference, options.height_reference, i, 0)
    draw_array(options.display, options.arrTexts, options.width_reference, options.height_reference)
    clock.tick(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = _Tela()
    clock.ticks.clear()
    options = HeapSortOptions(arr, textos, tela, 40, 100)
    simulate_heapsort(options)
    return arr, tela.quadros, list(clock.ticks)
