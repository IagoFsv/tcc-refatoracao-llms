class QuicksortParameter:
    def __init__(self, arr, arrTexts, display, width_reference, height_reference):
        self.arr = arr
        self.arrTexts = arrTexts
        self.display = display
        self.width_reference = width_reference
        self.height_reference = height_reference

def simulate_quicksort(param):
    partition(param.arr, param.arrTexts, param.display, param.width_reference, param.height_reference, 0, len(param.arr) - 1)
    draw_array(param.display, param.arrTexts, param.width_reference, param.height_reference)
    clock.tick(FREQUENCY_CLOCK)

def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = _Tela()
    clock.ticks.clear()
    param = QuicksortParameter(arr, textos, tela, 40, 100)
    simulate_quicksort(param)
    return arr, tela.quadros, list(clock.ticks)
