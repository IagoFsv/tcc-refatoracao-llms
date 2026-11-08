class Parameters:
    def __init__(self, arr, arrTexts, display, width_reference, height_reference, low, high):
        self.arr = arr
        self.arrTexts = arrTexts
        self.display = display
        self.width_reference = width_reference
        self.height_reference = height_reference
        self.low = low
        self.high = high

def simulate_quicksort(params):
    def partition(params):
        i = params.low - 1
        for j in range(params.low, params.high):
            if compare_elements(
                params.display, params.arrTexts, params.width_reference, params.height_reference, params.arr, j, params.high
            ):
                i += 1
                if i != j:
                    compare_and_swap(
                        params.display, params.arrTexts, params.width_reference, params.height_reference, params.arr, i, j
                    )
        if i + 1 != params.high:
            compare_and_swap(
                params.display, params.arrTexts, params.width_reference, params.height_reference, params.arr, i + 1, params.high
            )
        return i + 1

    def quicksort(params):
        if params.low < params.high:
            pi = partition(params)
            quicksort(
                Parameters(params.arr, params.arrTexts, params.display, params.width_reference, params.height_reference, params.low, pi - 1)
            )
            quicksort(
                Parameters(params.arr, params.arrTexts, params.display, params.width_reference, params.height_reference, pi + 1, params.high)
            )

    quicksort(params)
    draw_array(params.display, params.arrTexts, params.width_reference, params.height_reference)
    clock.tick(FREQUENCY_CLOCK)


def executar(valores):
    """Ordena uma copia de valores, animando cada passo. Ponto de entrada publico.

    Devolve uma tupla (lista ordenada, quadros desenhados, taxas dos ticks do relogio).
    Cada quadro e uma tupla (textos, posicoes destacadas, largura, altura).
    """
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = _Tela()
    clock.ticks.clear()
    simulate_quicksort(Parameters(arr, textos, tela, 40, 100, 0, len(arr) - 1))
    return arr, tela.quadros, list(clock.ticks)
