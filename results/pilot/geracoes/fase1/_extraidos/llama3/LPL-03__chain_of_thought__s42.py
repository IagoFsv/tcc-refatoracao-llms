class HeapifyParams:
    def __init__(self, arr, arrTexts, display, width_reference, height_reference, n, i):
        self.arr = arr
        self.arrTexts = arrTexts
        self.display = display
        self.width_reference = width_reference
        self.height_reference = height_reference
        self.n = n
        self.i = i

def heapify(params: HeapifyParams):
    largest = params.i
    l = 2 * params.i + 1
    r = 2 * params.i + 2
    if l < params.n and compare_elements(
        params.display, params.arrTexts, params.width_reference, params.height_reference, params.arr, largest, l
    ):
        largest = l
    if r < params.n and compare_elements(
        params.display, params.arrTexts, params.width_reference, params.height_reference, params.arr, largest, r
    ):
        largest = r
    if largest != params.i:
        compare_elements(
            params.display, params.arrTexts, params.width_reference, params.height_reference, params.arr, params.i, largest
        )
        swap_elements(params.arr, params.arrTexts, params.i, largest)
        heapify(HeapifyParams(params.arr, params.arrTexts, params.display, params.width_reference, params.height_reference, largest, largest))

def simulate_heapsort(arr, arrTexts, display, width_reference, height_reference):
    n = len(arr)
    for i in range(n, -1, -1):
        heapify(HeapifyParams(arr, arrTexts, display, width_reference, height_reference, n, i))
    for i in range(n - 1, 0, -1):
        swap_elements(arr, arrTexts, i, 0)
        heapify(HeapifyParams(arr, arrTexts, display, width_reference, height_reference, i, 0))
    draw_array(display, arrTexts, width_reference, height_reference)
    clock.tick(FREQUENCY_CLOCK)
