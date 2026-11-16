class Parameters:
    def __init__(self, textos, poses_elevated, width_rectangle, height_reference):
        self.textos = textos
        self.poses_elevated = poses_elevated
        self.width_rectangle = width_rectangle
        self.height_reference = height_reference


def draw_array(display, params):
    textos = tuple(texto.valor for texto in params.textos)
    display.quadros.append((textos, tuple(params.poses_elevated), params.width_rectangle, params.height_reference))


def swap_elements(arr, arrText, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arrText[i], arrText[j] = arrText[j], arrText[i]


def compare_elements(display, arrTexts, *args):
    params = Parameters(*args)
    draw_array(display, params)
    clock.tick(FREQUENCY_CLOCK)
    draw_array(display, params, [params.poses_elevated[0]])
    clock.tick(FREQUENCY_CLOCK)
    if (arr[params.poses_elevated[0]] > arr[params.poses_elevated[1]] and params.poses_elevated[0] < params.poses_elevated[1]) or (arr[params.poses_elevated[0]] < arr[params.poses_elevated[1]] and params.poses_elevated[0] > params.poses_elevated[1]):
        return False
    return True


def simulate_heapsort(arr, arrTexts, display, params):
    def heapify(arr, arrTexts, display, params, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and compare_elements(
            display, arrTexts, params.width_rectangle, params.height_reference, arr, largest, l
        ):
            largest = l
        if r < n and compare_elements(
            display, arrTexts, params.width_rectangle, params.height_reference, arr, largest, r
        ):
            largest = r
        if largest != i:
            compare_elements(
                display, arrTexts, params.width_rectangle, params.height_reference, arr, i, largest
            )
            swap_elements(arr, arrTexts, i, largest)
            heapify(
                arr, arrTexts, display, params.width_rectangle, params.height_reference, n, largest
            )

    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, arrTexts, display, params, n, i)
    for i in range(n - 1, 0, -1):
        swap_elements(arr, arrTexts, i, 0)
        heapify(arr, arrTexts, display, params, i, 0)
    draw_array(display, params)


def executar(valores):
    arr = list(valores)
    textos = [_Texto(str(x)) for x in arr]
    tela = _Tela()
    clock.ticks.clear()
    simulate_heapsort(arr, textos, tela, Parameters(40, 100, arr, []))
    return arr, tela.quadros, list(clock.ticks)
