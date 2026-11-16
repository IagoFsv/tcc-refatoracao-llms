class QuicksortParams:
    def __init__(self, arr, arrTexts, display, width_reference, height_reference):
        self.arr = arr
        self.arrTexts = arrTexts
        self.display = display
        self.width_reference = width_reference
        self.height_reference = height_reference

def simulate_quicksort(params):
    quicksort(params.arr, params.arrTexts, params.display, params.width_reference, params.height_reference, 0, len(params.arr) - 1)
    draw_array(params.display, params.arrTexts, params.width_reference, params.height_reference)
    clock.tick(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = _Tela()
    clock.ticks.clear()
    params = QuicksortParams(arr, textos, tela, 40, 100)
    simulate_quicksort(params)
    return arr, tela.quadros, list(clock.ticks)
